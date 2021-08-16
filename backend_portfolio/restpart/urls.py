from django.urls import path
from .views import *

urlpatterns = [
  path('feedback/', TypeFeedBackView.as_view()),
  path('feedback/create/', FeedBackCreateView.as_view()),
  path('feedback/<str:type_feedback>/', FeedBackView.as_view()),
  path('register/', UserCreate.as_view()),
  path('list/', UserList.as_view()),
  path('log/<str:username>/<str:password>/', UserLog.as_view()),
  path('title_creation/', TitleProjectCreate.as_view()),
  path('title_retrieve/<int:user>/', TitleProjectRetrieve.as_view()),
  path('task_creation/', TaskProjectCreate.as_view()),
  path('assignment_create/', AssignementProjectCreate.as_view()),
  path('assignment/', AssignementCreate.as_view()),
]

