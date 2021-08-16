from .serializers import *
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from userpart.models import *
from django.db.models import Q
import operator
import json
import sys
from functools import reduce
from django.shortcuts import get_object_or_404


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class FeedBackView(ListAPIView):
    serializer_class = FeedBackSerializer
    queryset = Feedback.objects.all()
    lookup_field = "type_feedback"

    def get_queryset(self):
        type_feedback = self.kwargs["type_feedback"]
        return Feedback.objects.filter(type_feedback=type_feedback)


# @method_decorator(csrf_exempt, name='dispatch')
class FeedBackCreateView(CreateAPIView):
    serializer_class = FeedBackSerializer
    queryset = Feedback.objects.all()
    permission_classes = (AllowAny,)

    def post(self,request):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({
                    "success": "Feedback Send Successfully",
                    "message": "Feedback accepted",
                    "object": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
                return Response({"error": "NOT OK"})

class TypeFeedBackView(ListCreateAPIView):
    serializer_class = TypeFeedBackSerializer
    queryset = TypeFeedBack.objects.all


class UserList(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class UserLog(ListAPIView, MultipleFieldLookupMixin):
    serializer_class = CustomUserSerializer
    lookup_field = ["username", "password"]

    def get_queryset(self):
        username = self.kwargs['username']
        password = self.kwargs['password']
        return CustomUser.objects.filter(username=username, password=password)


class UserLog2(RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    serializer_class = CustomUserSerializer
    lookup_field = ["username", "password"]

    def get_queryset(self):
        username = self.kwargs['username']
        password = self.kwargs['password']
        return CustomUser.objects.get(username=username, password=password)

    def get(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset)
        return Response({
                    json.dumps(serializer.data)
            }, status=status.HTTP_201_CREATED)


class UserCreate(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    # permission_classes = (AllowAny,)

    def post(self,request):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({
                    "success": "Account Successfully Created",
                    "message": "Registration accepted",
                    "object": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
                return Response({"error": "NOT OK"})


class TitleProjectCreate(ListCreateAPIView):
    serializer_class = TitleProjectSerializer
    queryset = TitleProject.objects.all()


class TaskProjectCreate(ListCreateAPIView):
    serializer_class = TaskProjectSerializer
    queryset = TaskProject.objects.all()


class AssignementCreate(ListCreateAPIView):
    serializer_class = AssignementSerializer
    queryset = Assignement.objects.all()


class AssignementProjectCreate(ListCreateAPIView):
    serializer_class = AssignementProjectSerializer
    queryset = Assignement.objects.all()


class TitleProjectRetrieve(ListAPIView):
    serializer_class = TitleProjectSerializer
    lookup_field = "user"


    def get_queryset(self, *args, **kwargs):
        user = self.kwargs["user"]
        print(user)
        user = "SELECT titles.id, titles.title, titles.user_id FROM userpart_titleproject AS titles, userpart_assignementproject AS projects WHERE titles.id = projects.project_id AND projects.user_id = %s" % user
        t = TitleProject.objects.raw(user)
        t = TitleProject.objects.filter(id__in=t.id)
        print(t, file=sys.stderr)
        return t


    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            projects = self.get_queryset()
            serializer = TitleProjectSerializer(projects)
            print(serializer)
            return Response({
                    json.dumps(serializer.data)
              }, status=status.HTTP_201_CREATED)











