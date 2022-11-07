from django.urls import path
from chat import views

urlpatterns = [
    path('', views.chatHome, name='chatHome'),
    path('<int:chat_id>',views.chatDetail,name='chatDetail'),
    path('ai',views.chatAI,name='chatAI'),
]
