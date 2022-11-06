from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('loginn/',views.login,name='login'),
    path('login/',views.loginHome,name='loginHome'),
    path('activate/<str:uid64>/<str:token>/',views.activate,name='activate'),
    path('delete/',views.delete, name='adelete'),
    path('loginerror/',views.loginerror, name='loginerror'),
    path('e400/',views.e400, name='e400'),
    path('e404/',views.e404, name='e404'),
    path('e500/',views.e500, name='e500'),
]
