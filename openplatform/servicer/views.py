#encoding=utf-8

import logging
from urllib import urlencode
import uuid

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from bixin.decorators import login_required
from bixin.helpers import get_random_str, create_signature, get_timestamp, format_transfer_protocol
from servicer.bot_service import BotService
from bixin.client import Client
from bixin.models import Deposit

@require_POST
@csrf_exempt
def bot_callback(request):
    bot = BotService(name=settings.APP_NAME, bot_access_token=settings.BOT_ACCESS_TOKEN,
                     bot_aes_key=settings.BOT_AES_KEY)
    return bot.process_main(request.body)

@login_required
def bot_detail(request):
    vendor_name = settings.APP_NAME
    user = request.bx_user
    target_id = user.target_id

    c = Client()
    jssdk_ticket = c.get_jsapi_ticket()['ticket']
    nonce = get_random_str()
    timestamp = get_timestamp()
    url = settings.JS_SDK_CALLBACK
    sign = create_signature(nonce=nonce, timestamp=timestamp,
                            url=url, jssdk_ticket=jssdk_ticket)

    currency = "BTC"

    #转发文章
    bot_target_id = settings.BOT_TARGET_ID # your bot target id
    share_url = 'https://bixin.im'
    share_title = '转发示例'
    share_desc = '转发示例'
    share_image_url = 'https://bixin.im/static/images/logo_slim@2x.d27f1d7c026c.png'

    # pay
    deposit_req = Deposit.objects.create(user=user)
    resp = c.get_vendor_address_list(currency='BTC')
    btc_address = resp.get('items', [])[0]

    # pay demo1
    amount = 0.001
    category = 'pay for test'

    #pay demo2
    order_id = uuid.uuid4().hex # 订单号，用户可自定义，最大长度是64
    transfer_type = 'spend'

    # pay demo3
    param2 = {
        'target_id': target_id,
        'conv_type': 'private',
        'amount': 1,
        'category': category,
    }
    protocol1 = format_transfer_protocol(None, 'AE', **param2)

    #pay demo4
    resp = c.get_vendor_address_list(currency='ETH')
    eth_address = resp.get('items', [])[0]
    param3 = {
        'amount': 0.01,
        'category': category,
        'order_id': order_id,
        'transfer_type': transfer_type,
        'x-name': 'test',
    }
    protocol2 = format_transfer_protocol(eth_address, 'ETH', **param3)

    #pay demo5
    # 如果order id 重复，所以转账后会提现付款已完成
    protocol3 = format_transfer_protocol(eth_address, 'ETH', **param3)

    return render(request, 'detail.html', locals())
