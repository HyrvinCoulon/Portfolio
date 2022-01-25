from django.contrib.auth.models import AbstractUser
from django.db import models
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.db.models import F


class TypeFeedBack(models.Model):
    name = models.CharField(primary_key=True, max_length=50)

    def __str__(self):
        return self.name


class Feedback(models.Model):

    username = models.CharField(max_length=50, default="")
    email = models.EmailField(default="", max_length=254)
    message = models.CharField(max_length=255, default="")
    type_feedback = models.ForeignKey(TypeFeedBack, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class User(AbstractUser):
    REQUIRED_FIELDS = ['email']

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    online = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def get_online(self):
        return self.online

    def set_online(self, cpt):
        self.online += cpt


class TitleProject(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def full_descrip(self):
        return f"title : {self.title} user : {self.user}"

    def __str__(self):
        return self.title


class TaskProject(models.Model):
    title = models.CharField(max_length=30, default="TaskModel")
    done = models.BooleanField(default=False)
    spent = models.FloatField(default=0)
    project = models.ForeignKey(TitleProject, on_delete=models.CASCADE)

    def set_spent(self, cpt):
        self.spent += cpt

    def get_spent(self):
        return self.spent

    def __str__(self):
        return self.title


class SubTaskProject(models.Model):
    title = models.CharField(max_length=30, default="SubTaskModel")
    fordate = models.DateField(default=None, blank=True, null=True)
    done = models.BooleanField(default=False)
    budget = models.FloatField(default=0)
    spent = models.FloatField(default=0)
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE)

    def set_spent(self, cpt):
        self.spent += cpt

    def get_spent(self):
        return self.spent

    def __str__(self):
        return self.title


class Assignement(models.Model):
    done = models.BooleanField(default=False)
    project = models.ForeignKey(SubTaskProject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    @property
    def full_describ(self):
        return f'project : {self.project.title} / done : {self.done}'


class AssignementProject(models.Model):
    project = models.ForeignKey(TitleProject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class MyConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        # Called when a new websocket connection is established
        print("connected", event)
        user = self.scope['user']
        self.update_user_status(user, 'online')

    async def websocket_receive(self, event):
        # Called when a message is received from the websocket
        # Method NOT used
        print("received", event)

    async def websocket_disconnect(self, event):
        # Called when a websocket is disconnected
        print("disconnected", event)
        user = self.scope['user']
        self.update_user_status(user, 'offline')

    @database_sync_to_async
    def update_user_status(self, user, status):
        """
        Updates the user `status.
        `status` can be one of the following status: 'online', 'offline' or 'away'
        """
        return User.objects.filter(pk=user.pk).update(status=status)

    @database_sync_to_async
    def update_user_incr(self, user):
        User.objects.filter(pk=user.pk).update(online=F('online') + 1)

    @database_sync_to_async
    def update_user_decr(self, user):
        User.objects.filter(pk=user.pk).update(online=F('online') - 1)
