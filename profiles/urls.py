from django.urls import path
from profiles import views

urlpatterns = [
    path('<str:user_name>/', views.profileHome, name='profileHome'),
    path('<str:user_name>/edit', views.profileEdit, name='profileEdit'),
    path('<str:username>/review', views.review, name='review'),
    path('userprofile/<str:username>', views.userProfile, name='userProfile'),
    path('userprofile/<str:username>/report', views.reportUser, name='reportUser'),
    path('<str:user_name>/sms', views.sms, name='sms'),
    path('checksms/<str:username>', views.checksms, name='checksms'),
    path('sendsms/<str:username>', views.sendsms, name='sendsms'),
    # path('<str:username>/report', views.reportUser, name='reportUser'),
    # path('<str:detale>/review', views.reportPost, name='reportPost'),
    # path('<str:username>/editreview', views.editreview, name='editreview'),
    # path('report/<str:username>', views.report, name='report'),

]
