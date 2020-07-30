from .models import *
from rest_framework import serializers


# This is the RESTapi function that reads the data
# from the WorkoutType, and print these workout exercises
# when users request it.
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutType
        fields = ('workout_name',)
