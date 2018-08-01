#encoding=utf-8

import logging
from urllib import urlencode
import uuid

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from bixin.decorators import login_required
from bixin.helpers import get_random_str, create_signature, get_timestamp, format_transfer_protocol, format_c2b_transfer_protocol, format_conversation_protocol
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
def jssdk_detail(request):
    vendor_name = settings.APP_NAME
    user = request.bx_user
    user_target_id = user.target_id

    bot_target_id = settings.BOT_TARGET_ID # your bot target id

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

    category = 'pay for test'
    amount = 0.001

    #pay demo2
    order_id = uuid.uuid4().hex # 订单号，用户可自定义，最大长度是64
    transfer_type = 'spend'

    return render(request, 'jssdk_detail.html', locals())

@login_required
def scheme_detail(request):
    vendor_name = settings.APP_NAME
    user = request.bx_user
    user_target_id = user.target_id
    bot_target_id = settings.BOT_TARGET_ID # your bot target id

    currency = "BTC"
    category = 'pay for test'

    # pay demo1
    amount = 0.001
    order_id = uuid.uuid4().hex # 订单号，用户可自定义，最大长度是64
    transfer_type = 'spend'

    param1 = {
        'target_id': user_target_id,
        'conv_type': 'private',
        'amount': 1,
        'category': category,
    }
    protocol1 = format_transfer_protocol(None, 'AE', **param1)

    #pay demo2
    c = Client()
    resp = c.get_vendor_address_list(currency='ETH')
    eth_address = resp.get('items', [])[0]
    param2 = {
        'amount': 0.01,
        'category': category,
        'order_id': order_id,
        'transfer_type': transfer_type,
        'x-name': 'test',
    }
    protocol2 = format_transfer_protocol(eth_address, 'ETH', **param2)

    protocol3 = format_conversation_protocol(user_target_id, 'private')
    protocol4 = format_conversation_protocol(bot_target_id, 'bot', 'test', 'action_demo')

    protocol5 = format_c2b_transfer_protocol('c2bTransfer', eth_address, 'ETH', 'c2b pay demo', amount, memo='')
    protocol6 = format_c2b_transfer_protocol('c2bDeposit', eth_address, 'ETH', 'c2b deposit demo', memo='')

    return render(request, 'scheme_detail.html', locals())
