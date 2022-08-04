from django.urls import path
from buy import views

urlpatterns = [
    path('',views.buyHome , name='buyHome'),
    path('category/<str:category>/',views.p_category, name='category'),
    path('create',views.buyCreate , name='buyCreate'),
    path('detail/<int:post_id>',views.buyDetail,name='buyDetail'),
     path('detail/<int:post_id>/delete',views.buyDelete,name='buyDelete'),
    path('detail/<int:post_id>/edit',views.buyEdit,name='buyEdit'),

    # path('auth/',views.auth , name='auth'),
    # path('join/<str:user_id>',views.join , name='join'),

  #  path('',views.createpur),

]