from django.urls import path
from .views import *

urlpatterns = [
  path('feedback/', TypeFeedBackSerializer.as_view()),
  path('feedback/<str:type_feedback>/', Feedback.as_view()),
]
    
