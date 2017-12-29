#encoding=utf-8

import logging
import re
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def login_required(func):
    def __w(request, *args, **kw):
        if not request.bx_user.is_authenticated():
            return redirect('/')
        else:
            return func(request, *args, **kw)
    return __w

MOBILE_USER_AGENTS =  'palm|blackberry|nokia|phone|midp|mobi|symbian|chtml|ericsson|minimo|' + \
                      'audiovox|motorola|samsung|telit|upg1|windows ce|ucweb|astel|plucker|' + \
                      'x320|x240|j2me|sgh|portable|sprint|docomo|kddi|softbank|android|mmp|' + \
                      'pdxgw|netfront|xiino|vodafone|portalmmm|sagem|mot-|sie-|ipod|up\\.b|' + \
                      'webos|amoi|novarra|cdm|alcatel|pocket|iphone|mobileexplorer|mobile'

def tag_device(func):
    def __w(request, *args, **kw):
        agent = request.META.get('HTTP_USER_AGENT','')
        if re.search(MOBILE_USER_AGENTS, agent, re.I):
            request.from_device = 'phone'
        else:
            request.from_device = 'pc' # or ipad
        return func(request, *args, **kw)

    return __w


