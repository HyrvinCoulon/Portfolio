from django.urls import path
from .views import *


urlpatterns = [
  path('feedback/', TypeFeedBackView.as_view()),
  path('feedback/create/', FeedBackCreateView.as_view()),
  path('feedback/<str:type_feedback>/', FeedBackView.as_view()),
  path('register/', UserCreate.as_view()),
  path('list/', UserList.as_view()),
  path('log/<str:username>/<str:password>/', UserLog2.as_view()),
  path('log/<str:username>/<str:password>/update/', UserLog2.as_view()),
  path('logout/<str:username>/<str:password>/', UserOut.as_view()),
  path('title_creation/', TitleProjectCreate.as_view()),
  path('title_retrieve/<int:user>/', TitleProjectRetrieve.as_view()),
  path('assigntitle/<int:user>/', AssignTitle.as_view()),
  path('title_profile/<int:user>/', TaskProfile.as_view()),
  path('title_RUD/<int:id>/update/', TitleRUD.as_view()),
  path('task_retrieve/<int:user>/<int:title_project>/', TaskProjectRetrieve.as_view()),
  path('task_creation/', TaskProjectCreate.as_view()),
  path('subtask_creation/', SubTaskProjectCreate.as_view()),
  path('tasklead/<int:title_project>/<int:user>/', TaskLeadProjectRetrieve.as_view()),
  path('taskspent/<int:id>/<int:project>/', TaskSpent.as_view()),
  path('taskscheck/', SubTaskCheck.as_view()),
  path('task_RUD/<int:id>/update/', TaskRUD.as_view()),
  path('subtask_RUD/<int:id>/update/', SubTaskRUD.as_view()),
  path('subtask_notification/<int:uid>/', SubstakRetrieve.as_view()),
  path('usermember_retrieve/<int:title_project>/', UserRetrieve.as_view()),
  path('assignment_create/', AssignementProjectCreate.as_view()),
  path('assignment/', AssignementCreate.as_view()),
]


