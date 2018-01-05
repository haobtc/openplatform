#encoding=utf-8

import uuid
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from bixin.helpers import ok_json, error_json, format_transfer_protocol
from bixin.decorators import login_required
from bixin.client import Client

from bixin.models import Deposit
from assets.forms import WithdrawForm, form_error_formatter

@login_required
def request_deposit(request):
    user = request.bx_user
    currency = 'BTC'

    client = Client()
    resp = client.get_vendor_address_list(currency=currency)
    vendor_addresses = resp.get('items', [])

    if len(vendor_addresses) == 0:
        return error_json(error='vendor does not have address for %s' % currency)

    vendor_address = vendor_addresses[0]

    deposit = Deposit.objects.create(user=user)

    transfer_protocal = format_transfer_protocol(
        target_addr=vendor_address,
        currency=currency,
        category='deposit',
        args={'deposit_id': deposit.id}
    )

    return ok_json(result=transfer_protocal)

@login_required
def deposit_process(request):
    deposit_id = request.GET.get('deposit_id')
    if not deposit_id:
        return error_json('missing deposit_id')

    try:
        deposit = Deposit.objects.get(pk=deposit_id)
    except Deposit.DoesNotExist:
        return error_json('deposit request not found')

    if deposit.status == "SUCCESS":
        return ok_json(result='success')
    else:
        return ok_json(result='pending')

@csrf_exempt
@require_POST
@login_required
def request_withdraw(request):
    user = request.bx_user

    form = WithdrawForm(request.POST, user=user)
    if form.is_valid():
        form.save()
        resp = 'success'
    else:
        errors = form_error_formatter(form.errors)
        return error_json(error=errors)
    return ok_json(result=resp)
