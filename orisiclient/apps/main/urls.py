from django.conf.urls import patterns, url

from views import (
    MainPageView,
    FAQView,
    TimelockView,
    TimelockRetrieveView,
    GetTimelockForAddress)

urlpatterns = patterns('',
    url(r'^faq$', FAQView.as_view(), name='faq'),
    url(r'^timelock$', TimelockView.as_view(), name='timelock'),
    url(r'^timelock_wait$', TimelockRetrieveView.as_view(), name='timelock-retrieve'),
    url(r'^get_timelock_for_address', GetTimelockForAddress.as_view(), name='timelock-addr'),
    url(r'^$', MainPageView.as_view(), name='main'),
)
