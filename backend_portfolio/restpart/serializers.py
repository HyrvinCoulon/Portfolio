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


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'username', 'email', 'password', 'online']
        model = models.User

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


class TitleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.TitleProject


class TaskProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.TaskProject


class SubTaskProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = models.SubTaskProject


class AssignementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Assignement


class AssignementProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.AssignementProject
