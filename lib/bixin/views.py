# -*- coding: utf-8 -*-
import time
import logging
from datetime import timedelta
import json

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from bixin.models import Event
from bixin.crypt import Prpcrypt
from bixin.helpers import ok_json, error_json

from bixin.event_handlers import CallbackHandler

@require_POST
@csrf_exempt
def event_callback(request):

    # 回调过程如果使用了加密， 则需要进行解密
    # 如果没有涉及到加密，则直接使用

    raw_body = request.body.decode('utf-8')

    try:
        if settings.VENDOR_AES_KEY:
            prpcrypt = Prpcrypt(settings.VENDOR_AES_KEY)
            raw_body = prpcrypt.decrypt(raw_body)
        body = json.loads(raw_body)
    except Exception as e:
        logging.info(e)
        return error_json('request data is not valid')

    event_id = body.get('event_id')
    subject = body.get('subject')
    if not event_id or not subject:
        return error_json('missing params')

    event, created = Event.objects.get_or_create(event_id=event_id,
                                                 subject=subject,
                                                 defaults={
                                                     'content': json.dumps(body.get('payload')),
                                                 })

    if not created and event.status == 'PROCESSED':
        return error_json('already processed')

    handler = CallbackHandler(event)
    resp = handler.process_event()

    return resp
