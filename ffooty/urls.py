from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include, reverse_lazy

from ffooty.views import (IndexView, LoginView, LogoutView,
                          AuctionFileUploadView, PlayerUpdateFileUploadView)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password/change/',
         PasswordChangeView.as_view(
             template_name='password_change.html',
             success_url=reverse_lazy('logout'),
         ),
         name='password_change'),
    path('auction_file_upload/',
         AuctionFileUploadView.as_view(),
         name='auction_file_upload'),
    path('player_table_file_upload/',
         PlayerUpdateFileUploadView.as_view(),
         name='player_file_upload'),
                       
    path('api/', include('ffooty.api_urls')),

    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),
]
