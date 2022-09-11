from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('login/',views.login,name='login'),
    path('activate/<str:uid64>/<str:token>/',views.activate,name='activate'),
    path('checksms/', views.SMSVerificationView.as_view(), name='checksms'),
    path('sendsms/', views.SmsSendView.as_view(), name='sendsms'),
    
]
