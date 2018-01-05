# -*- coding: utf-8 -*-
import time
import logging
from datetime import timedelta
import json
from urllib import urlencode

from django.conf import settings
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from bixin.helpers import utc_now
from bixin.client import Client
from bixin.decorators import login_required, tag_device
from bixin.models import QRSession, Fund
from bixin.helpers import ok_json, error_json
from bixin.bot import Bot
from bixin.helpers import ok_json, error_json

@tag_device
def home(request):
    if request.bx_user.is_authenticated():
        return redirect(reverse('account:index'))

    bot_token = request.GET.get('bot_token')
    if bot_token:
        return bot_login(request, bot_token)

    return render(request, 'home.html', locals())

@login_required
def index(request):
    user = request.bx_user
    funds = Fund.objects.filter(user=user)
    if not funds:
        fund = Fund.objects.create(user=user)
    else:
        fund = funds.first()

    return render(request, 'index.html', locals())

def bot_login(request, bot_token):

    bot = Bot()
    expire = 60 * 60 * 24
    platform_user_id = bot.valid_token(bot_token, expire=expire)
    if not platform_user_id:
        logging.warn("Invalid  bot_token {} return 401".format(bot_token))
        return error_json('Invalid bot token', status=401)

    c = Client()
    user = c.get_user(platform_user_id, cache=True)

    request.session['expire'] = int(time.time()) + expire
    request.session['site_userid'] = user.id
    site_userid = user.id

    return redirect(reverse('account:index'))

@tag_device
def qr_session(request):
    uuid = request.GET.get('uuid')
    sys_vendor_name = settings.APP_NAME
    if uuid:
        qr_info = uuid.split(':')
        if len(qr_info) < 2:
            return error_json('qr code format error')
        vendor_name, uuid = qr_info[:2]
        try:
            qr_session = QRSession.objects.get(uuid=uuid)
        except QRSession.DoesNotExist:
            return error_json('qr code not found')

        if vendor_name != sys_vendor_name:
            return error_json('vendor not match')

        elif qr_session.is_expired():
            return error_json('qr code expired')

        elif qr_session.user:
            request.session['site_userid'] = qr_session.user.id
            return ok_json(result='success')

        elif qr_session.user is None:
            return error_json('no user found')

        else:
            return error_json('fail')
    else:
        expire_seconds = 60 * 3
        qr_session = QRSession.objects.create(expired_at=utc_now() + timedelta(seconds=expire_seconds))

        QR_LOGIN_URL = settings.QR_LOGIN_URL
        protocol = "{}/qrcode/?uuid={}:{}".format(QR_LOGIN_URL, sys_vendor_name, qr_session.uuid)

        if request.from_device == 'phone':
            protocol = "bixin://login/confirm?{}".format(urlencode({'url': protocol}))

        resp = {
            'protocol': protocol,
            'expired_at': qr_session.expired_at.isoformat()
        }

    return ok_json(result=resp)

@login_required
def logout(request):
    request.session.flush()
    return redirect(reverse('home'))
