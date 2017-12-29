from django.conf.urls import url

from servicer.views import bot_callback, bot_detail

urlpatterns = [
    url(r'^callback/', bot_callback, name='bot_callback'),
    url(r'^detail/', bot_detail, name='bot_detail'),
]
