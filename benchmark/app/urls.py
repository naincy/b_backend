from django.urls import path
from app import views

"""
API's for the Benchmark Application
"""
urlpatterns = [
    path('authenticate_user', views.authenticate_user, name="authenticate_user"),
    path('register_user', views.register_user, name="register_user"),
    path('users', views.users, name="list_users"),
    path('users/<str:user>', views.users, name="get_user"),
    path('user', views.updateUser, name="update_user"),
    path('feedback', views.saveFeedback, name="save_feedBack")
]