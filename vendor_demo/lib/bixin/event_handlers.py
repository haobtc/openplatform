# -*- coding: utf-8 -*-
import logging
import json

from django.conf import settings
from django.db import transaction

from bixin.helpers import ok_json, error_json
from bixin.client import Client
from bixin.models import QRSession, User
from bixin.synchronizers import sync_transfer_to_deposit

class CallbackHandler(object):

    def __init__(self, event):
        self.event = event

    def process_event(self):
        handler = self.get_event_handler(self.event.subject)
        if not handler:
            return error_json('unknown event %s' % self.event.subject)

        self.client = Client()
        with transaction.atomic():
            resp = handler()
            self.event.status = 'PROCESSED'
            self.event.save()

        return resp

    def get_event_handler(self, subject):
        event_handlers = {
            'vendor_qr_login': self.process_qr_login,
            'user2vendor.created': self.process_platform_deposit,
        }
        return event_handlers.get(subject)

    def process_qr_login(self):
        content = json.loads(self.event.content)
        user_id = content.get('user_id')
        if not user_id:
            return error_json('missing user id in platform event')

        qr_uuid = content.get('qr_uuid')
        if not qr_uuid:
            return error_json('missing qr uuid in platform event')

        try:
            qr_session = QRSession.objects.get(uuid=qr_uuid)
        except QRSession.DoesNotExist:
            return error_json('qr code not found')

        if qr_session.user:
            return error_json('qr code used')

        if qr_session.is_expired():
            return error_json('qr code expired')

        else:
            user, user_info = self.client.fetch_user(user_id)
            qr_session.user = user
            qr_session.save()

            return ok_json(result='success')

    def process_platform_deposit(self):
        sync_transfer_to_deposit()
        return ok_json(result='suucess')
