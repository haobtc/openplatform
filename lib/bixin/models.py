import json
import decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from bixin.fields import JSONField
from bixin.fields import BixinDecimalField
from bixin.base_models import BaseModel
from bixin import helpers

class User(BaseModel):
    userid = models.IntegerField(unique=True)
    username = models.CharField(max_length=200, blank=True, null=True, default='')
    target_id = models.CharField(max_length=32, unique=True, null=True)

    def is_authenticated(self):
        return True

class Token(BaseModel):
    token = models.CharField(max_length=200, blank=True, null=True)
    expired_at = models.DateTimeField(null=True, blank=True)

class Withdraw(BaseModel):
    STATUS_CHOICES = [(x, x) for x in ['PENDING', 'SENT']]
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='PENDING')
    amount = BixinDecimalField(default=0)
    user = models.ForeignKey(User, related_name='withdraws')

    def get_payload(self):
        data = {
            'currency': 'BTC',
            'category': 'Test for demo',
            'amount': str(self.amount),
            'client_uuid': self.uuid,
            'user': self.user.userid,
        }
        return data

class Deposit(BaseModel):
    STATUS_CHOICES = [(x, x) for x in ['PENDING', 'SUCCESS']]
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='PENDING')
    amount = BixinDecimalField(default=0)
    user = models.ForeignKey(User, related_name='deposit')

class Fund(BaseModel):
    user = models.ForeignKey(User, related_name='funds', db_index=True)
    balance = BixinDecimalField(default=0)

class Event(BaseModel):
    STATUS_CHOICES = [(x, x) for x in ['RECEIVED', 'PROCESSED']]
    event_id = models.IntegerField(db_index=True)
    subject = models.CharField(max_length=32, db_index=True)
    content = JSONField(default={}, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='RECEIVED', db_index=True)

class QRSession(BaseModel):
    expired_at = models.DateTimeField(db_index=True)
    user = models.ForeignKey(User, null=True)

    def is_expired(self):
        return self.expired_at < helpers.utc_now()


