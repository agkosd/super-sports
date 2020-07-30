# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Create your models here.

# UserStates table contains user, DOB, and height fields.
# Users can use this UserStats to get the basic information they entered
class UserStats(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    DOB = models.DateField(default=datetime.date.today())
    height = models.FloatField(default=0)


# Update_user_profile provides a functionality of letting user edit their profile
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)
    instance.userstats.save()


# WorkoutType is a model that let admin user to type in what kind of workout types are available to record for users
class WorkoutType(models.Model):
    workout_name = models.CharField(max_length=100, primary_key=True)

    # Return the workout name when referencing
    def __str__(self):
        return self.workout_name


# WeightGoals model is designed for letting user type in their weight target
class WeightGoals(models.Model):
    username = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    weight_target = models.FloatField(default=0)


# FatGoals model is designed for letting user type in their fat target
class FatGoals(models.Model):
    username = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    fat_target = models.FloatField(default=0)

# StrengthGoals model is designed for letting user select the workout type
# and type in the target weight for that workout
class StrengthGoals(models.Model):

    username = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    workout_name = models.ForeignKey(WorkoutType, on_delete=models.CASCADE, default='Other')
    strength_target = models.FloatField(default=0)

# TDEE model is designed for letting user type in their Total Daily Energy Expenditure
# And their recomended intake can be calculated for any goal they may want to achieve
class TDEE(models.Model):
    username = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    tdee = models.FloatField(default=0)
    goal = models.CharField(max_length=100)


# StrengthWorkout model is designed for letting user record their detailed workout
# info from workout type, which includes data, sets, reps, and weight for the selected workout

class StrengthWorkout(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_name = models.ForeignKey(WorkoutType, on_delete=models.CASCADE)
    workout_date = models.DateTimeField('date workout')
    sets = models.IntegerField(default=0, validators=[MaxValueValidator(20), MinValueValidator(0)])
    reps = models.IntegerField(default=0, validators=[MaxValueValidator(50), MinValueValidator(0)])
    workout_weight = models.FloatField(default=0, validators=[MaxValueValidator(500), MinValueValidator(0)])
    ORM = models.FloatField(default=0)


# StatsOverTime model is designed for recording users' stats and display them with graphs
class StatsOverTime(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('date stats')
    bodyweight = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    calorie_intake = models.FloatField(default=0)
