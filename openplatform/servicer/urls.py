from django.conf.urls import url

from servicer.views import bot_callback, jssdk_detail, scheme_detail

urlpatterns = [
    url(r'^callback/', bot_callback, name='bot_callback'),
    url(r'^jssdk_detail/', jssdk_detail, name='jssdk_detail'),
    url(r'^scheme_detail/', scheme_detail, name='scheme_detail'),
]
