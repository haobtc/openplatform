# -*- coding: utf-8 -*-
import re
import hashlib
import json
import logging
import pytz
import datetime
import decimal
import random
import string
import time

from urllib import urlencode
from django.http import JsonResponse

def format_transfer_protocol(target_addr, currency,
                             target_id=None, conv_type="private",
                             amount=None, category=None,
                             order_id=None, transfer_type=None,
                             **kw):
    if target_addr:
        params = {
            'target_addr': target_addr,
        }
    else:
        params = {
            'target_id': target_id,
            'conv_type': conv_type,
        }

    if currency:
        params['currency'] = currency
        if amount:
            params['amount'] = amount

    if category:
        params['category'] = category

    if order_id:
        params['order_id'] = order_id

    if transfer_type:
        params['transfer_type'] = transfer_type

    if kw:
        # 用户定义参数
        for k, w in kw.iteritems():
            if re.match('^x-', k):
                params.update({k: w})

    protocal = 'bixin://currency_transfer/?%s' % (urlencode(params))

    return protocal


def format_c2b_transfer_protocol(scheme_path, target_addr, currency, message, amount=None, memo=''):
    params = {
        'target_addr': target_addr,
        'currency': currency,
        'message': message,
        'memo': memo
    }

    if scheme_path == 'c2bTransfer':
        params['amount'] = amount

    protocal = 'bixin://transfer/%s?%s' % (scheme_path, urlencode(params))

    return protocal


def format_conversation_protocol(target_id, conv_type, text='', event=None):
    params = {
        'target_id': target_id,
        'conv_type': conv_type
    }

    if text:
        params.update({'text': text})

    if event and text:
        params.update({
            'event': event
        })

    protocol = 'bixin://conversation/?%s' % (urlencode(params))
    return protocol

def ok_json(**kw):
    kw['ok'] = True
    return JsonResponse(kw)

def error_json(error, status=200):
    resp = {'ok': False,  'error': error}
    return JsonResponse(resp, status=status)

def utc_now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

def floor_decimal(amount, digits=8):
    return amount.quantize(
        decimal.Decimal('1E-%d' % digits),
        context=decimal.Context(rounding=decimal.ROUND_FLOOR))

def parse_decimal(v, default='0', digits=8):
    try:
        return floor_decimal(decimal.Decimal(v), digits=digits)
    except decimal.InvalidOperation:
        return decimal.Decimal(default)

def create_signature(**kw):
    params = sorted(kw.items())
    url_encode = urlencode(params)

    h = hashlib.sha1()
    h.update(url_encode)
    sig = h.hexdigest()
    return sig

def get_random_str():
    rule = string.ascii_letters + string.digits
    str = random.sample(rule, 8)
    return "".join(str)

def get_timestamp():
    t = time.time()
    return int(t)
