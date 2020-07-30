from django.contrib import admin
from .models import UserStats, WorkoutType, WeightGoals, FatGoals, StrengthGoals, StrengthWorkout, StatsOverTime


# admin.py is designed for registering all of the models so that we can use them in the admin page
# admin.site.register(User)
admin.site.register(UserStats)
admin.site.register(WorkoutType)
admin.site.register(WeightGoals)
admin.site.register(FatGoals)
admin.site.register(StrengthGoals)
admin.site.register(StrengthWorkout)
admin.site.register(StatsOverTime)
