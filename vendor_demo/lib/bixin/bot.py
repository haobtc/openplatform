# -*- coding: utf-8 -*-
import re
import logging
import uuid
import base64
import json
import time
import random
import requests

from urlparse import urljoin
from urllib import unquote
from urllib import urlencode

from django.utils.translation import ugettext as _
from django.http import JsonResponse
from django.conf import settings
from django.utils import translation

from bixin.crypt import Prpcrypt
from bixin.helpers import ok_json, error_json

class Bot(object):
    def __init__(self, name=settings.APP_NAME, bot_access_token=settings.BOT_ACCESS_TOKEN,
                       bot_aes_key=settings.BOT_AES_KEY):
        self.name = name
        self.bot_access_token = bot_access_token
        self.bot_aes_key = bot_aes_key

        self.pc = Prpcrypt(self.bot_aes_key)
        self.evt = None

    def api_post(self, url, data, headers=None, timeout=120):
        if headers is None:
            headers = {}

        if not settings.BIXIN_APP_HOST:
            logging.error('not set BIXIN_APP_HOST for test')
            return {"ok": True }

        url = urljoin(settings.BIXIN_APP_HOST, url)

        b = '{}:{}'.format(self.name, self.bot_access_token)
        a = base64.encodestring(b.encode('utf-8')).strip()

        headers['Authorization'] = 'Basic {}'.format(a)
        headers['User-Agent'] = 'Bot/{}'.format(self.name)

        s_time = time.time()
        resp = requests.post(url, data=data, headers=headers, timeout=timeout)

        e_time = time.time()
        logging.info('bot->web <%s> post <%s> duration %s'%(url, data, e_time-s_time))
        if resp.status_code == 502:
            msg = '{} response status: {} {}'.format(
                url, resp.status_code, resp.content)
            raise ResponseBadStatus(msg)

        try:
            resp_json = json.loads(resp.content)
            if 'ok' not in resp_json or not resp_json['ok']:
                logging.error("bixin: Bot {} send api_post failed: {}".format(self.name, resp.content))
            return resp_json
        except ValueError:
            logging.error("bixin: {} return {} {}".format(url, resp.status_code, resp.content))
            raise Exception('{} response status: {} {}'.format(url, resp.status_code, resp.content))

    def api_get(self, url, params, headers=None, timeout=10):
        if headers is None:
            headers = {}

        if not settings.BIXIN_APP_HOST:
            logging.error('not set BIXIN_APP_HOST for test')
            return {"ok": True }

        url = urljoin(settings.BIXIN_APP_HOST, url)

        b = '{}:{}'.format(self.name, self.bot_access_token)
        a = base64.encodestring(b.encode('utf-8')).strip()

        headers['Authorization'] = 'Basic {}'.format(a)
        headers['User-Agent'] = 'Bot/{}'.format(self.name)

        s_time = time.time()
        resp = _session.get(url, params=params, headers=headers, timeout=timeout)

        e_time = time.time()
        logging.info('bot->web <%s> get <%s> duration %s' % (url, params, e_time - s_time))
        if resp.status_code == 502:
            msg = '{} response status: {} {}'.format(
                url, resp.status_code, resp.content)
            raise ResponseBadStatus(msg)

        try:
            resp_json = json.loads(resp.content)
            if 'ok' not in resp_json or not resp_json['ok']:
                logging.error("bixin: Bot {} send api_get failed: {}".format(self.name, resp.content))
            return resp_json
        except ValueError:
            logging.error("bixin: {} return {} {}".format(url, resp.status_code, resp.content))
            raise Exception('{} response status: {} {}'.format(url, resp.status_code, resp.content))

    def valid_token(self, encrypt_token, expire=120):
        encrypt_token = unquote(encrypt_token)
        try:
            json_data = self.decrypt_data(encrypt_token)
            dict_data = json.loads(json_data)
        except:
            logging.error('decrypt data is error')
            return None

        user_id = dict_data.get('user_id', '')
        timestamp = dict_data.get('timestamp', '')

        logging.info('timestamp %s, user_id %s'%(timestamp, user_id))
        if not timestamp:
            logging.warn('bad timestamp %s'%(timestamp))
            return None
        if not user_id:
            logging.warn('invalid user id %s'%(user_id))
            return None
        now = int(time.time())
        if not timestamp or (int(timestamp) + expire < now):
            if timestamp:
                logging.warn('expire token %s + %s < %s = %s'%(timestamp, expire, now, (int(timestamp) + expire < now)))
            logging.warn('invalid timestamp %s'%(timestamp))
            return None

        return user_id

    def decrypt_data(self, encrypt_data):
        descrypt_data = self.pc.decrypt(encrypt_data) #解密
        return  descrypt_data

    def _get_event(self, data):
        evt = BotEvent()
        try:
            req_data = json.loads(data)
            encrypt_content = req_data['data']
        except KeyError:
            return None
        try:
            json_data = self.decrypt_data(encrypt_content)

            dict_data = json.loads(json_data)
        except:
            import traceback
            traceback.print_exc()
            return None

        try:
            evt.event = dict_data['event']
            evt.data = dict_data['data']
            evt.to_bot = self
            self.evt = evt
        except KeyError:
            return None

        return self.evt

    def process_main(self, encrypted_data):
        ''' The main entry for handel the request'''
        evt = self._get_event(encrypted_data)
        if not evt:
            return error_json('auth failed', status=401)
        return self.process_msg()

    def process_msg(self):
        if self.evt.event not in ['msg', 'welcome']:
            return error_json('not support event: %s'%self.evt.event)

        if self.evt.event == 'welcome':
            self.welcome_msg()
            return ok_json()

        content_type = self.evt.data['content_type']

        if content_type == 'event':
            self.process_event_msg()
        elif content_type == 'text':
            self.process_text_msg()
        elif content_type == 'image':
            self.process_image_msg()
        return ok_json()

    def process_event_msg(self):
        pass

    def process_image_msg(self):
        pass

    def process_text_msg(self):
        pass

    def send_text_msg(self, text, target_id=None):
        if target_id is None:
            target_id = self.evt.data['sender']['id']

        data = {
            'request_id': str(uuid.uuid4().hex),
            'target_id': target_id,
            'text': text
        }

        return self.send_bot_msg('/api/v2/bot.postText', data, msg_format='form')

    def send_bot_msg(self, msg_router, data, msg_format='json'):
        lang = translation.get_language()
        headers = {
            "Accept-Language": lang
        }

        if 'request_id' not in data:
            data['request_id'] = str(uuid.uuid4().hex)

        if msg_format == 'json':
            headers['Accept'] = "application/json"
            headers['Content-Type'] = "application/json;charset=utf-8"
            post_data = json.dumps(data, encoding="utf-8")
        else:
            post_data = data

        return self.api_post(msg_router, post_data, headers=headers)

    def send_set_bot_menu(self, data):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8'
        }
        post_data = json.dumps(data, encoding="utf-8")
        return self.api_post('/api/v2/bot.setMenu', post_data, headers=headers)

    # other apis

class BotEvent:
    def __init__(self):
        pass
