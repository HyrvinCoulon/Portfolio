from django.contrib.auth import authenticate
from django.db import Error
from django.db.models.expressions import RawSQL
from django.http import JsonResponse

from .serializers import *
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import json
from django.shortcuts import get_object_or_404

from userpart.models import *


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
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

    def post(self, request):
        if request.method == "POST":
            print(request.data)
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            print(serializer.data)
            return Response({
                "success": "Feedback Send Successfully",
                "message": "Feedback accepted",
                "object": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "NOT OK"})


class TypeFeedBackView(ListCreateAPIView):
    serializer_class = TypeFeedBackSerializer
    queryset = TypeFeedBack.objects.all()


class UserList(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()


class UserOut(UpdateAPIView, MultipleFieldLookupMixin):
    serializer_class = CustomUserSerializer
    lookup_field = ["username", "password"]

    def get_queryset(self):
        username = self.kwargs['username']
        password = self.kwargs['password']
        user = authenticate(username=username, password=password)
        return user

    def update(self, request, *args, **kwargs):

        if request.method == "PUT":
            queryset = self.get_queryset()
            # print(type(queryset))
            queryset.set_online(-1)
            # print(queryset.get_online())
            data = {"online": queryset.get_online()}
            serializer = CustomUserSerializer(queryset, data=data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            # print(serializer.data)

            return Response(serializer.data)


class UserLog2(RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    serializer_class = CustomUserSerializer
    lookup_field = ["username", "password"]

    def get_queryset(self):
        username = self.kwargs['username']
        password = self.kwargs['password']
        user = authenticate(username=username, password=password)
        return user

    def get_object(self):
        queryset = self.get_queryset()
        # make sure to catch 404's below
        # print(queryset)
        obj = queryset
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            queryset = self.get_queryset()
            queryset.set_online(1)
            data = {"online": queryset.get_online()}
            serializer = CustomUserSerializer(queryset, data=data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
            # print(serializer.data)
            return JsonResponse({
                "user": json.dumps(serializer.data)
            }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # print("OBJ update kwargs= %s , data = %s" % (kwargs, str(request.data)))

        if request.method == "PUT":
            instance = self.get_object()
            data = None
            if request.data.get('username') is not None:
                data = {'username': request.data.get('username')}
            if request.data.get('email') is not None:
                data = {'email': request.data.get('email')}

            serializer = self.get_serializer(instance, data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            instance = self.get_object()
            data = self.perform_destroy(instance)
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class UserCreate(CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    # permission_classes = (AllowAny,)

    def post(self, request):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)

            return Response({
                "success": "Account Successfully Created",
                "message": "Registration accepted",
                "object": serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "NOT OK"})


class UserRetrieve(ListAPIView):
    serializer_class = CustomUserSerializer
    lookup_field = "title_project"

    def get_queryset(self, *args, **kwargs):
        title_project = self.kwargs["title_project"]
        user_query = "SELECT users.id FROM userpart_user AS users, " \
                     "userpart_assignementproject AS projects WHERE " \
                     "projects.project_id = %s AND projects.user_id = users.id"
        return User.objects.filter(id__in=RawSQL(user_query, [title_project]))


class TitleProjectCreate(ListCreateAPIView):
    serializer_class = TitleProjectSerializer
    queryset = TitleProject.objects.all()


class TaskProjectCreate(ListCreateAPIView):
    serializer_class = TaskProjectSerializer
    queryset = TaskProject.objects.all()

    def create(self, request, *args, **kwargs):
        if request.method == "POST":
            # print(request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            # print(type(serializer.data))
            return JsonResponse({
                "success": serializer.data
            }, safe=False, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": "NOT OK"})


class SubTaskProjectCreate(ListCreateAPIView):
    serializer_class = SubTaskProjectSerializer
    queryset = SubTaskProject.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                d = dict(serializer.data)
                TaskProject.objects.filter(id=d['project']).update(done=False)
                print(d)
                print(serializer.data)
                return JsonResponse({
                    "success": serializer.data
                }, safe=False, status=status.HTTP_201_CREATED)
        except Error as err:
            print(err)
            return JsonResponse({"error": "NOT OK"})


class SubstakRetrieve(ListAPIView):
    serializer_class = SubTaskProjectSerializer
    queryset = SubTaskProject.objects.all()
    lookup_field = ["uid"]

    def get(self, request, *args, **kwargs):

        if request.method == "GET":
            uid = self.kwargs["uid"]
            if uid is not None:
                user_query = "SELECT titles.id FROM userpart_subtaskproject AS titles, " \
                             "userpart_assignement AS project WHERE project.user_id = %s AND " \
                             "titles.id = project.project_id "
                queryset = SubTaskProject.objects.filter(id__in=RawSQL(user_query, [uid]))
                serializers_list = SubTaskProjectSerializer(queryset, many=True)
                return JsonResponse({
                    "tasks": serializers_list.data
                }, safe=False, status=status.HTTP_201_CREATED)
            else:
                queryset = SubTaskProject.objects.all()
                return JsonResponse({
                    "tasks": queryset
                }, safe=False, status=status.HTTP_201_CREATED)


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
        # print(user)
        user_query = "SELECT titles.id FROM userpart_titleproject AS titles WHERE titles.user_id = %s "

        t = TitleProject.objects.filter(id__in=RawSQL(user_query, [user]))
        # for c in t:
        #    print(c.title)
        return t


class AssignTitle(ListAPIView, ):
    serializer_class = TitleProjectSerializer
    lookup_field = "user"

    def get_queryset(self, *args, **kwargs):
        user = self.kwargs["user"]
        # print(user)
        user_query = "SELECT titles.id FROM userpart_titleproject AS titles, " \
                     "userpart_assignementproject AS projects WHERE projects.user_id = %s AND " \
                     "titles.id = projects.project_id "

        t = TitleProject.objects.filter(id__in=RawSQL(user_query, [user]))
        return t


class TaskProjectRetrieve(ListAPIView, MultipleFieldLookupMixin):
    serializer_class = SubTaskProjectSerializer
    lookup_field = ["user", "title_project"]

    def get_queryset(self, *args, **kwargs):
        user = self.kwargs["user"]
        title_project = self.kwargs["title_project"]

        user_query = "SELECT titles.id FROM userpart_subtaskproject AS titles, userpart_taskproject AS tasks, " \
                     "userpart_assignement AS projects, userpart_titleproject AS entitle WHERE entitle.id = %s AND " \
                     "tasks.project_id = entitle.id AND tasks.id = titles.project_id AND titles.id = " \
                     "projects.project_id AND " \
                     "projects.user_id = %s "
        verification_query = "SELECT assign.id FROM userpart_assignement AS assign, userpart_subtaskproject AS titles," \
                             " userpart_titleproject AS entitle, userpart_taskproject AS tasks  WHERE entitle.id = %s " \
                             "AND tasks.project_id = entitle.id AND tasks.id = titles.project_id AND " \
                             "assign.project_id = " \
                             "titles.id AND assign.user_id = %s "
        task_assign = "SELECT tasks.id FROM userpart_titleproject AS titles,userpart_taskproject AS tasks, " \
                      "userpart_assignementproject AS projects WHERE projects.user_id = %s AND " \
                      "titles.id = projects.project_id AND tasks.project_id = titles.id"
        a = Assignement.objects.filter(id__in=RawSQL(verification_query, [title_project, user]))
        t = SubTaskProject.objects.filter(id__in=RawSQL(user_query, [title_project, user]), ).order_by('fordate')
        task = TaskProject.objects.filter(id__in=RawSQL(task_assign, [user]))
        # print(a)
        # print(t)
        # print(task)
        for c in t:
            for ass in a:
                if c.done != ass.done and c.id == ass.project.id:
                    c.done = ass.done
                    break
        return t, task

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            serializer_sub, serializer_tasks = self.get_queryset()
            serializer_sub = SubTaskProjectSerializer(serializer_sub, many=True)
            serializer_tasks = TaskProjectSerializer(serializer_tasks, many=True)
            return JsonResponse({
                "tasks": serializer_tasks.data,
                "sub": serializer_sub.data
            }, safe=False, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": "NOT OK"})


class TaskLeadProjectRetrieve(ListAPIView, MultipleFieldLookupMixin):
    serializer_class = TaskProjectSerializer
    lookup_field = ["user", "title_project"]

    def get_queryset(self, *args, **kwargs):
        title_project = self.kwargs["title_project"]
        user = self.kwargs["user"]
        user_query = "SELECT titles.id FROM userpart_taskproject AS titles,userpart_titleproject AS entitle WHERE " \
                     "entitle.id = %s AND titles.project_id = entitle.id "
        subtask_query = "SELECT subtasks.id FROM userpart_titleproject AS titles, userpart_taskproject AS tasks, " \
                        "userpart_subtaskproject AS subtasks WHERE titles.user_id = %s AND titles.id = " \
                        "tasks.project_id AND tasks.id = subtasks.project_id "
        t = TaskProject.objects.filter(id__in=RawSQL(user_query, [title_project]))
        st = SubTaskProject.objects.filter(id__in=RawSQL(subtask_query, [user])).order_by('fordate')
        print(t)
        print(st)
        # for c in t:
        #    print(c.title)
        return st, t

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            serializer_sub, serializer_tasks = self.get_queryset()
            serializer_sub = SubTaskProjectSerializer(serializer_sub, many=True)
            serializer_tasks = TaskProjectSerializer(serializer_tasks, many=True)
            # print(type(serializer.data))
            return JsonResponse({
                "tasks": serializer_tasks.data,
                "sub": serializer_sub.data
            }, safe=False, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": "NOT OK"})


class TaskSpent(UpdateAPIView, MultipleFieldLookupMixin):
    serializer_class = SubTaskProjectSerializer
    lookup_field = ["id", "project"]

    def get_queryset(self):
        id = self.kwargs['id']
        project = self.kwargs["project"]
        t = SubTaskProject.objects.filter(id=id).update(budget=self.request.data.get("budget"), spent=F("spent") + 10)
        task = TaskProject.objects.filter(id=project).update(spent=F("spent") + 10)
        return t

    def update(self, request, *args, **kwargs):
        # print("OBJ update kwargs= %s , data = %s" % (kwargs, str(request.data)))

        if request.method == "PUT":
            t = self.get_queryset()
            return Response(t)


class TitleRUD(RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    queryset = TitleProject.objects.all()
    serializer_class = TitleProjectSerializer
    lookup_field = "id"

    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        # print(self.kwargs["id"])
        obj = queryset.get(id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        # print("OBJ update kwargs= %s , data = %s" % (kwargs, str(request.data)))

        if request.method == "PUT":
            instance = self.get_object()
            data = {'title': request.data.get('title')}
            serializer = self.get_serializer(instance, data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)


class TaskRUD(RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    queryset = TaskProject.objects.all()
    serializer_class = TaskProjectSerializer
    lookup_field = "id"

    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(id=self.kwargs["id"])
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        # print("OBJ update kwargs= %s , data = %s" % (kwargs, str(request.data)))

        if request.method == "PUT":
            instance = self.get_object()
            data = None
            if request.data.get('title') is not None and request.data.get('fordate') is not None:
                data = {'title': request.data.get('title'), 'fordate': request.data.get('fordate')}
            elif request.data.get('fordate') is not None:
                data = {'fordate': request.data.get('fordate')}
            else:
                data = {'title': request.data.get('title')}
            serializer = self.get_serializer(instance, data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            instance = self.get_object()
            data = self.perform_destroy(instance)
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class SubTaskRUD(RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    queryset = SubTaskProject.objects.all()
    serializer_class = SubTaskProjectSerializer
    lookup_field = "id"

    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        id = self.kwargs["id"]
        return SubTaskProject.objects.filter(id=id).first()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        # print("OBJ update kwargs= %s , data = %s" % (kwargs, str(request.data)))

        if request.method == "PUT":
            instance = self.get_object()
            data = None
            if request.data.get('title') is not None and request.data.get('fordate') is not None:
                data = {'title': request.data.get('title'), 'fordate': request.data.get('fordate')}
            elif request.data.get('fordate') is not None:
                data = {'fordate': request.data.get('fordate')}
            else:
                data = {'title': request.data.get('title')}
            serializer = self.get_serializer(instance, data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        if request.method == "DELETE":
            instance = self.get_object()
            data = self.perform_destroy(instance)
            return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class SubTaskCheck(UpdateAPIView, MultipleFieldLookupMixin):
    lookup_field = ["project", "user"]
    serializer_class = AssignementSerializer

    def get_queryset(self, *args, **kwargs):
        project = self.request.data.get("project")
        user = self.request.data.get("user")
        print("OBJ update kwargs= %s , data = %s" % (kwargs, str(self.request.data)))
        done = False
        if self.request.data.get("done") == "true":
            done = True
        ta = Assignement.objects.filter(project=project, user=user).update(done=done)
        t = Assignement.objects.get(project=project, user=user)
        print(type(t))
        if not done:
            SubTaskProject.objects.filter(id=t.project.id).update(done=done)
            subs = SubTaskProject.objects.get(id=t.project.id)
            task = TaskProject.objects.filter(id=subs.project.id).update(done=done)
        # print(id)
        return t

    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            queryset = self.get_queryset()
            assignement = Assignement.objects.filter(project=self.request.data.get("project"))
            sub = SubTaskProject.objects.get(id=self.request.data.get("project"))
            t = TaskProject.objects.get(id=sub.project.id)
            subs = SubTaskProject.objects.filter(project=t.id)

            for assign in assignement:
                if not assign.done:
                    return Response({"user": "notcheck"})

            sub.done = True
            sub.save()
            print(subs)
            for subt in subs:
                if not subt.done:
                    return Response({"user": "Sub Task notcheck"})

            t.done = True
            t.save()
            return Response({"user": "Main Task Check"})


class TaskProfile(MultipleFieldLookupMixin, ListAPIView):
    serializer_class = TitleProjectSerializer
    queryset = TitleProject.objects.all()
    lookup_fields = ["user", "title_project"]

    def get_queryset(self):
        # title_project = self.kwargs["title_project"]
        user = self.kwargs["user"]
        user_query = "SELECT DISTINCT entitle.id FROM " \
                     "userpart_titleproject AS entitle,  userpart_assignement assign WHERE " \
                     "assign.user_id = %s OR " \
                     "entitle.user_id = %s "
        t = TitleProject.objects.filter(id__in=RawSQL(user_query, [user, user]))
        # for c in t:
        #    print(c.title)
        return t
