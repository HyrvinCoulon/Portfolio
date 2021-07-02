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
