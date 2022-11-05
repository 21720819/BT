from django.contrib import admin
from django.urls import path,include,re_path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

import accounts.views as cv
from django.conf.urls import handler400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('',views.home, name='home'),

    path('free/',include('free.urls')),
    path('buy/',include('buy.urls')),
    path('chat/',include('chat.urls')),
    path('profile/',include('profiles.urls')),
    path('password_reset/', cv.UserPasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', cv.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', cv.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', cv.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # re_path(r'^accounts/', include('accounts.urls')),
    # re_path(r'^accounts/', include('allauth.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler500 = 'accounts.views.custom_500_error'
handler404 = 'accounts.views.custom_404_error'
handler400 = 'accounts.views.custom_400_error'