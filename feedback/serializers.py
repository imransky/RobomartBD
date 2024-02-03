from rest_framework import serializers
from django.db.models import QuerySet
from rest_framework.fields import empty
from .models import Feedback
from Basic_Api.serializers import UserCreateSerializer

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(many=False)
    class Meta:
        model = Feedback
        fields = '__all__'



