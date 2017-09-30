from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import password_change, password_change_done

from ffooty.views import (IndexView, LoginView, LogoutView,
                          AuctionFileUploadView, PlayerUpdateFileUploadView)

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/password/change/$', password_change,
            {'template_name': 'password_change.html', 
             'post_change_redirect': 'home'}, 
             name='password_change'),
    url(r'^auction_file_upload/',
        AuctionFileUploadView.as_view(),
        name='auction_file_upload'),
    url(r'^player_table_file_upload/',
        PlayerUpdateFileUploadView.as_view(),
        name='player_file_upload'),
                       
    url(r'^api/', include('ffooty.api_urls')),

    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
)

