import decimal
import json
from django import template
from bitcoin.core import COIN

from bixin import helpers

register = template.Library()

@register.filter(name='dformat')
def dformat(value, currency='BTC'):
    if isinstance(value, basestring) or value is None:
        value = helpers.parse_decimal(value)

    if currency in ('BTC',):
        hold_len = 8
        fmt = '%i.%08i'
        k = COIN
    else:
        hold_len = 2
        fmt = '%i.%02i'
        k = 100

    sign = ''
    if value < 0:
        value = -value
        sign = '-'

    upv = value * (10 ** hold_len)

    r = fmt % (upv // k, upv % k)
    r = sign + r.rstrip('0').rstrip('.')
    if r == '-0':
        r = '0'
    return r

@register.filter(name='json2str')
def json2str(j):
    return json.dumps(j)

