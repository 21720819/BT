from django.urls import path
from free import views

urlpatterns = [
    path('',views.freeHome, name = 'freeHome'),
    path('create/', views.freeCreate, name='freeCreate'),
    path('detail/<int:free_id>', views.freeDetail, name='freeDetail'),
    path('create_comment/<int:free_id>',views.create_comment, name='create_comment'),
    path('detail/<int:free_id>/delete',views.freeDelete,name='freeDelete'),
    path('detail/<int:free_id>/edit',views.freeEdit,name='freeEdit'),
]
