"""openplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from assets.views import request_deposit, request_withdraw, deposit_process

urlpatterns = [
    url(r'^request_deposit/$', request_deposit, name='request_deposit'),
    url(r'^request_withdraw/$', request_withdraw, name='request_withdraw'),
    url(r'^deposit_process/$', deposit_process, name='deposit_process'),
]
