from django.contrib import admin
from django.urls import path,include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),
    path('free/',include('free.urls')),
    path('buy/',include('buy.urls')),
    path('chat/',include('chat.urls')),
]
