from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.chatbot_api, name='chatbot_api'),
    path('api/schedule/', views.get_training_schedule, name='training_schedule'),
    path('api/plans/', views.get_membership_plans, name='membership_plans'),
]