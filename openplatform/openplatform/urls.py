from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from account.views import home
from bixin.views import event_callback

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^assets/', include('assets.urls', namespace='assets')),
    url(r'^bot/', include('servicer.urls', namespace='servicer')),
    url(r'^event_callback', event_callback, name='event_callback'),
] + staticfiles_urlpatterns()
