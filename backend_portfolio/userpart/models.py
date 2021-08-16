from django.db import models


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

class CustomUser(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class TitleProject(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TaskProject(models.Model):
    title = models.CharField(max_length=30)
    fordate = models.DateField(default=None)
    project = models.ForeignKey(TitleProject, on_delete=models.CASCADE)


class Assignement(models.Model):
    project = models.ForeignKey(TaskProject, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class AssignementProject(models.Model):
    project = models.ForeignKey(TitleProject, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


