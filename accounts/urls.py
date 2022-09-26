from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('loginn/',views.login,name='login'),
    path('login/',views.loginHome,name='loginHome'),
    path('activate/<str:uid64>/<str:token>/',views.activate,name='activate'),

    
]
