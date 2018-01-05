# -*- coding: utf-8 -*-
import logging
from decimal import Decimal

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from bixin.models import Withdraw, Fund
from bixin.client import Client

AMOUNT_EMPTY_ERROR = _('Amount cannot be empty')
AMOUNT_NEGATIVE_ERROR = _('Amount must be positive')
AMOUNT_NOT_ENOUGH = _('Amount must be enough')
AMOUNT_TOO_SMALL_ERROR = _('Amount needs be greater than %s')

def form_error_formatter(error_massages):
    """Format Django form errors into a dict object."""
    error_list = []
    for item, message in error_massages.iteritems():
        if len(message) == 1:
            description = message[0]
        else:
            description = message
        error_list.append(description)

    return error_list

class WithdrawForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WithdrawForm, self).__init__(*args, **kwargs)

    amount = forms.DecimalField()

    def clean(self):
        amount = self.cleaned_data.get('amount')

        if not amount:
            raise forms.ValidationError(AMOUNT_EMPTY_ERROR)

        if amount <= 0:
            raise forms.ValidationError(AMOUNT_NEGATIVE_ERROR)

        fund = Fund.objects.select_for_update().filter(user=self.user).first()
        if fund.balance < amount:
            raise forms.ValidationError(AMOUNT_NOT_ENOUGH)

        return self.cleaned_data

    def save(self):
        amount = self.cleaned_data['amount']

        with transaction.atomic():

            withdraw = Withdraw.objects.create(user=self.user, amount=amount)

            fund = Fund.objects.select_for_update().filter(user=self.user).first()
            balance = fund.balance - amount
            fund.balance = balance
            fund.save()
            logging.info('fund %s decr balance %s, remain=%s', fund.id, amount, balance)

            c = Client()
            c.send_withdraw(withdraw)

            return withdraw
