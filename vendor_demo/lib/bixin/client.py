import urllib
import requests
import uuid
import json
from datetime import timedelta
from django.utils import timezone
from urlparse import urljoin
from django.conf import settings
from bixin.models import Token, User

PLATFORM_SERVER = getattr(settings, 'PLATFORM_SERVER', 'http://localhost:8000/platform/')

class APIError(Exception):
    def __init__(self, code, msg):
        self.code = code
        super(APIError, self).__init__(msg)

class Client(object):
    def __init__(self, app_name=settings.APP_NAME, secret=settings.VENDOR_SECRET):
        self.vendor_name = app_name
        self.secret = secret

    def get_access_token(self):
        now = timezone.now()
        token = Token.objects.filter(expired_at__gt=now).last()
        if not token:
            path = '/platform/token?vendor=%s&secret=%s' % (self.vendor_name,
                                                            self.secret)
            url = urljoin(PLATFORM_SERVER, path)
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                a = r.json()
                expired_at = now + timedelta(seconds=a['expire_in'])
                access_token = a['access_token']
                token = Token.objects.create(token=access_token,
                                                     expired_at=expired_at)
            else:
                raise APIError(r.status_code, {'text': r.text})
        return token

    def request_platform(self, method, path, params=None, client_uuid=None):
        if params is None:
            params = {}
        token = self.get_access_token()
        params['access_token'] = token.token

        url = urljoin(PLATFORM_SERVER, path)

        kw = {}
        kw['timeout'] = 15

        if method == 'GET':
            body = urllib.urlencode(params)
            if body:
                url = '%s?%s' % (url, body)
            r = requests.get(url, **kw)
        else:
            # POST
            cu = params.get('client_uuid', client_uuid) or uuid.uuid4().hex
            params['client_uuid'] = cu
            kw['data'] = params
            r = requests.post(url, **kw)

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 400:
            jsonr = r.json()
            if 'access_token' in jsonr:
                Token.objects.all().delete()
                return self.request_platform(method, path, params=params)
            raise APIError(r.status_code, jsonr)
        else:
            raise APIError(r.status_code, r.text)

    def get_user_obj(self, user_info):
        defaults = {
            'username': user_info['username'],
            'target_id': user_info['target_id'],
        }

        u, _ = User.objects.update_or_create(userid=user_info['id'], defaults=defaults)
        return u

    def get_user(self, userid, cache=False):
        if cache:
            user = User.objects.filter(userid=userid).first()
            if user:
                return user
        user_info = self.request_platform('GET', '/platform/api/v1/user/%s' % userid)
        return self.get_user_obj(user_info)

    def get_user_list(self, offset=0, limit=100):
        params = {
            'offset': offset,
            'limit': limit,
        }
        return self.request_platform('GET', '/platform/api/v1/list', params=params)

    def get_transfer(self, client_uuid):
        return self.request_platform('GET', '/platform/api/v1/transfer/item',
                                     {'client_uuid': client_uuid})

    def get_transfer_list(self, offset=0, limit=100, status=None, type=None, order='asc'):
        return self.request_platform('GET', '/platform/api/v1/transfer/list',
                                     {'offset': offset,
                                      'limit': limit,
                                      'status': status,
                                      'type': type,
                                      'order': order
                                  })

    def send_withdraw(self, withdraw):
        assert withdraw.status == 'PENDING'
        r = self.request_platform('POST',
                                  '/platform/api/v1/withdraw/create',
                                  withdraw.get_payload())
        withdraw.status = 'SENT'
        withdraw.save()
        return r

    def get_vendor_address_list(self, currency='BTC', offset=0, limit=20):
        params = {
            'offset': offset,
            'limit': limit,
            'currency': currency
        }
        return self.request_platform('GET', '/platform/api/v1/address/list', params)

    def fetch_user(self, userid):
        user_info = self.request_platform('GET', '/platform/api/v1/user/%s' % userid)
        user = self.get_user_obj(user_info)
        return user, user_info

    def get_jsapi_ticket(self):
        return self.request_platform('GET', '/platform/api/v1/ticket/jsapi')

    def pull_event(self, since_id, limit=20):
        payload = {'since_id': since_id, 'limit': limit}
        return self.request_platform('GET', '/platform/api/v1/event/list', payload)
