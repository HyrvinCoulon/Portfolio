from django.urls import path
from .views import *

urlpatterns = [
  path('feedback/', TypeFeedBackView.as_view()),
  path('feedback/<str:type_feedback>/', FeedBackView.as_view()),
]
    
