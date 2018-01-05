"""Sync tools."""
import json
import decimal
import logging
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from bixin.client import Client
from bixin.models import Deposit, Fund

def sync_transfer_to_deposit():
    c = Client()
    resp = c.get_transfer_list(status='SUCCESS', limit=10, type='deposit', order='desc')
    logging.info('get transfer %s', resp)
    for transfer in resp['items']:
        user = c.get_user(transfer['user.id'], cache=True)
        deposit_id = transfer['args'].get('deposit_id')
        amount=decimal.Decimal(transfer['amount'])

        if not deposit_id:
            continue

        with transaction.atomic():
            try:
                deposit = Deposit.objects.select_for_update().get(pk=deposit_id, user=user)
            except Deposit.DoesNotExist:
                continue

            if deposit.status != 'PENDING':
                continue

            fund = Fund.objects.select_for_update().filter(user=user).first()
            balance = fund.balance + amount
            fund.balance = balance
            fund.save()
            deposit.amount = amount
            deposit.status = 'SUCCESS'
            deposit.save()

            logging.info('asset fund %s incr balance %s, new=%s', fund.id, amount, balance)

