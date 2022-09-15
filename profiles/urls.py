from django.urls import path
from profiles import views

urlpatterns = [
    path('<str:user_name>/', views.profileHome, name='profileHome'),
    path('userprofile/<str:username>', views.userProfile, name='userProfile'),
    path('<str:user_name>/sms', views.sms, name='sms'),
    path('checksms/<str:username>', views.checksms, name='checksms'),
    path('sendsms/<str:username>', views.sendsms, name='sendsms'),

]
