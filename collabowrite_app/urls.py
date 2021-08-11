from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.index),
    path('directory', views.directory),
    path('topic/<topic>', views.topic),
    path('board/<int:board_id>', views.display_board),

    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('create_board', views.create_board),
    path('create_section', views.create_section),
    path('board/<int:board_id>/<int:section_id>/delete_section', views.delete_section),
    path('board/<int:board_id>/<int:section_id>/display_create_post', views.display_create_post),
    path('create_post', views.create_post),
    path('board/<int:board_id>/delete_board', views.delete_board),
    path('board/<int:board_id>/<int:post_id>/display_post', views.display_post),
    path('board/<int:board_id>/<int:post_id>/delete_post', views.delete_post),
]