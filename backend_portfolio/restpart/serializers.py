from django.db.models import fields
from userpart import models
from rest_framework import serializers


class TypeFeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.TypeFeedBack

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Feedback
