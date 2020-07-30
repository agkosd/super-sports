from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.utils.decorators import method_decorator
# from .models import Login
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from .models import *
from django.views.generic import ListView, UpdateView, DeleteView
from django.utils import formats
from . import serializers
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse


# Home page, also the index page
def Home(request):
    if request.user.is_authenticated:
        current_user = request.user
        stats = {}
        context = {}

        # Generating and populating weight progress
        if WeightGoals.objects.filter(username=current_user).exists():
            context['weight_progress'] = current_user.weightgoals.weight_target
            weights = StatsOverTime.objects.filter(username=current_user).order_by('-date')
            if len(weights) > 0:
                context['weight'] = weights[0].bodyweight

        # Generating and populating fat progress
        if FatGoals.objects.filter(username=current_user).exists():
            context['fat_progress'] = current_user.fatgoals.fat_target
            fats = StatsOverTime.objects.filter(username=current_user).order_by('-date')
            if len(fats) > 0:
                context['fat'] = fats[0].fat

        # Generating and populating strength progress
        if StrengthGoals.objects.filter(username=current_user).exists():
            context['strength_progress'] = current_user.strengthgoals.strength_target
            context['exersize'] = current_user.strengthgoals.workout_name

        # Generating and populating strength progress
        if TDEE.objects.filter(username=current_user).exists():
            context['tdee'] = current_user.tdee.tdee
            context['tdee_target'] = current_user.tdee.goal

        form = SelectExe(request.POST)
        if form.is_valid():
            work_type = form.cleaned_data.get('workout_name')
            print(work_type)
            # filters data by user then filter that by workout, then gsort in ascending mode
            Workout_stats = StrengthWorkout.objects.filter(username=request.user).filter(workout_name=work_type).filter(workout_weight__gt = 0).order_by('workout_date')
            Workout_stats_count = Workout_stats.count()

            if Workout_stats_count > 5:
                # filters data by user then filter that by workout, then get the latetest 5 and sort in ascending mode
                Workout_stats = StrengthWorkout.objects.filter(username=request.user).filter(workout_name=work_type).filter(workout_weight__gt = 0).order_by('-workout_date')[:5:-1]
                Workout_stats_count = 5



            for i in range(0, Workout_stats_count):
                stats['weight' + str(i)] = Workout_stats[i].workout_weight
                stats['date' + str(i)] = Workout_stats[i].workout_date.date()
                if Workout_stats[i].reps == 0:
                    stats['rm' + str(i)] = 0
                else:
                    stats['rm' + str(i)] = (Workout_stats[i].workout_weight) / (0.0278 * (Workout_stats[i].reps))
            stats['workout_count'] = Workout_stats_count
        else:
            form = SelectExe()

        # user stats graph
        body_weight = StatsOverTime.objects.filter(username=current_user).filter(bodyweight__gt = 0).order_by('date')
        body_weight_count = body_weight.count()
        if body_weight_count > 5:
            body_weight_count = 5
            body_weight = StatsOverTime.objects.filter(username=current_user).filter(bodyweight__gt = 0).order_by('-date')[:5:-1]

        for i in range(0, body_weight_count):
            stats['bodyweight' + str(i)] = body_weight[i].bodyweight
            stats['fat' + str(i)] = body_weight[i].fat
            stats['cal' + str(i)] = body_weight[i].calorie_intake
            stats['user_date' + str(i)] = body_weight[i].date.date()
        stats['user_count'] = body_weight_count

        return render(request, "fitness_app/home.html", {'stats': stats, 'form': form, 'context': context})
    else:
        return render(request, 'fitness_app/index.html', None)


@login_required
def Profile(request):
    current_user = request.user
    stats = {}
    weights = StatsOverTime.objects.filter(username=current_user).order_by('-date')
    if len(weights) > 0:
        stats['weight'] = weights[0].bodyweight
    stats['age'] = current_user.userstats.DOB
    stats['height'] = current_user.userstats.height
    if TDEE.objects.filter(username=current_user).exists():
        stats['tdee'] = current_user.tdee.tdee

    return render(request, "fitness_app/profile.html", {'stats': stats})


# Edit goals page. Here multiple forms for each goal is shown and can be saved.
@login_required
def EditGoals(request):
    current_user = request.user
    if request.method == 'POST':

        # Checking if the weight form is submitted
        if 'weight_target' in request.POST:
            weightForm = WeightForm(request.POST)
            if weightForm.is_valid():
                post = weightForm.save(commit=False)
                post.username = current_user
                post.save()
                print("saved weight")
        else:
            # Generating and populating weight target form
            if WeightGoals.objects.filter(username=current_user).exists():
                weightForm = WeightForm(initial={'weight_target': current_user.weightgoals.weight_target})
            else:
                weightForm = WeightForm()

        # Checking if the fat form is submitted
        if 'fat_target' in request.POST:
            fatForm = FatForm(request.POST)
            if fatForm.is_valid():
                post = fatForm.save(commit=False)
                post.username = current_user
                post.save()
        else:
            # Generating and populating fat target form
            if FatGoals.objects.filter(username=current_user).exists():
                fatForm = FatForm(initial={'fat_target': current_user.fatgoals.fat_target})
            else:
                fatForm = FatForm()

        # Checking if the fat form is submitted
        if 'strength_target' in request.POST:
            strengthForm = StrengthForm(request.POST)
            if strengthForm.is_valid():
                post = strengthForm.save(commit=False)
                post.username = current_user
                post.save()
        else:
            # Generating and populating strength target form
            if StrengthGoals.objects.filter(username=current_user).exists():
                strengthForm = StrengthForm(initial={'workout_name': current_user.strengthgoals.workout_name,
                                                     'strength_target': current_user.strengthgoals.strength_target})
            else:
                strengthForm = StrengthForm()

        # Checking if the TDEE form is submitted
        if 'tdee' in request.POST:
            tdeeForm = TDEEForm(request.POST)
            if tdeeForm.is_valid():
                post = tdeeForm.save(commit=False)
                post.username = current_user
                post.save()
        else:
            # Generating and populating TDEE target form
            if TDEE.objects.filter(username=current_user).exists():
                tdeeForm = TDEEForm(initial={'tdee':current_user.tdee.tdee,'goal':current_user.tdee.goal})
            else:
                tdeeForm = TDEEForm()

        # Generating context and rendering page
        context = {
            'weightForm':weightForm,
            'fatForm':fatForm,
            'strengthForm':strengthForm,
            'tdeeForm':tdeeForm
        }
        return render(request, "fitness_app/editgoals.html", context)

    # If it is not a post then generate the forms with defaults and render the page
    else:
        # Generating and populating weight target form
        if WeightGoals.objects.filter(username=current_user).exists():
            weightForm = WeightForm(initial={'weight_target': current_user.weightgoals.weight_target})
        else:
            weightForm = WeightForm()

        # Generating and populating fat target form
        if FatGoals.objects.filter(username=current_user).exists():
            fatForm = FatForm(initial={'fat_target': current_user.fatgoals.fat_target})
        else:
            fatForm = FatForm()

        # Generating and populating strength target form
        if StrengthGoals.objects.filter(username=current_user).exists():
            strengthForm = StrengthForm(initial={'workout_name': current_user.strengthgoals.workout_name,
                                                 'strength_target': current_user.strengthgoals.strength_target})
        else:
            strengthForm = StrengthForm()

        # Generating and populating TDEE target form
        if TDEE.objects.filter(username=current_user).exists():
            tdeeForm = TDEEForm(initial={'tdee':current_user.tdee.tdee,'goal':current_user.tdee.goal})
        else:
            tdeeForm = TDEEForm()

        context = {
            'weightForm':weightForm,
            'fatForm':fatForm,
            'strengthForm':strengthForm,
            'tdeeForm':tdeeForm
        }
        return render(request, "fitness_app/editgoals.html", context)

# Editing user stats. This does not require password input
@login_required
def editProfile(request):
    current_user = request.user

    if request.method == 'POST':
        # Find form that is posted

        form = ProfileForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()

            # after editing their info, it will redirect to the profile page
            return redirect('../profile/')
        context = {
            "form": form
        }
        return render(request, "fitness_app/editprofile.html", context)
    else:
        form = ProfileForm(initial={'DOB': current_user.userstats.DOB, 'height': current_user.userstats.height})

        context = {
            "form": form
        }
        return render(request, "fitness_app/editprofile.html", context)


# Editing the user values this requires a password input
@login_required
def editUser(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, user=current_user)
        if form.is_valid():

            # if password authentication succeeds, then users will be able to change their information
            if authenticate(username=current_user.username, password=form.cleaned_data.get('password')):
                changeUser = User.objects.get(username=current_user)
                changeUser.first_name = form.cleaned_data.get('first_name')
                changeUser.last_name = form.cleaned_data.get('last_name')
                changeUser.email = form.cleaned_data.get('email')
                changeUser.save()

                # after editing their info, it will redirect to the profile page
            return redirect('../profile/')
        context = {
            "form": form
        }
        return render(request, "fitness_app/editprofile.html", context)

    # if post is not requested, then it will just show the current information that users previously typed in.
    else:
        form = UserEditForm(initial={'first_name': current_user.first_name, 'last_name': current_user.last_name,
                                     'email': current_user.email}, user=current_user)

        context = {
            "form": form
        }
        return render(request, "fitness_app/editprofile.html", context)


'''
Generates the Strength Standards page
'''


@login_required
def StrengthStandards(request):
    # gets the logged in user as an object
    current_user = request.user
    stats = {}

    # Queries the fitness_app and retrieve the bodyweight of the logged-in user
    weights = StatsOverTime.objects.filter(username=current_user).order_by('-date')
    if len(weights) > 0:
        stats['weight'] = weights[0].bodyweight

    # render the strengthstandards page and send the user's bodyweight for use in the webpage
    return render(request, "fitness_app/strengthstandards.html", {'stats': stats})


# Signup page. A valid height and date of birth is required for a valid acconut creation.
def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user first, so that a height and DOB can be generated for it.
            user = form.save()
            user.save()
            user.refresh_from_db()
            # Add the user height and DOB to the seperate table.
            user.userstats.height = form.cleaned_data.get('height')
            user.userstats.DOB = form.cleaned_data.get('DOB')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            # Log the user in after a successful account creation.
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # Redirect them to the profile page.
            return redirect('../profile/')
    else:
        # On a get request, generate and return the signup form.
        form = SignUpForm()
    return render(request, 'fitness_app/signup.html', {'form': form})


# This is a Json response for use with AJAX to check if a username is taken.
def ValidateUsername(request):
    # Gets the username from the request
    username = request.GET.get('username', None)
    data = {'taken': User.objects.filter(username__iexact=username).exists()}

    # If the username is taken save an error message
    if data['taken']:
        data['message'] = 'Already taken, Sorry!'
    return JsonResponse(data)


# logger
@login_required
def Logger(request):
    template_name = 'fitness_app/logger.html'
    model = StrengthWorkout
    if request.method == 'POST':
        form = LoggerForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.save()
            return redirect('list/')

        return render(request, template_name, {'form': form})
    else:
        form = LoggerForm()
        return render(request, template_name, {'form': form})


# logger
@login_required
def Statsovertime(request):
    current_user = request.user
    template_name = 'fitness_app/statsovertime.html'
    if request.method == 'POST':
        form = StatsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = current_user
            post.save()
            return redirect('stats/')

        return render(request, template_name, {'form': form})
    else:
        # Populates the form with values from the previous stats info.
        currentStats = StatsOverTime.objects.filter(username=current_user).order_by('-date')
        if len(currentStats) > 0:
            form = StatsForm(initial={'bodyweight': currentStats[0].bodyweight, 'fat': currentStats[0].fat,
                                      'calorie_intake': currentStats[0].calorie_intake})
        else:
            form = StatsForm()
        return render(request, template_name, {'form': form})


# This is the view method for showing the signUp infomation
# After users sign up, it is gonna redirect to the signup form and show the sign up info
def SignUpinfo(request):
    template_name = 'fitness_app/SignUpinfo.html'
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.username = request.user
            post.save()

        return render(request, template_name, {'form': form})
    else:
        form = ProfileForm()
        return render(request, template_name, {'form': form})

#uses class based views so that the django default listview,updateview,deleteview could be utilised for
#displaying the logs and allowing the user to update or delete them
@method_decorator(login_required, name='dispatch')
class LoggerList(ListView):
    model = StrengthWorkout
    template_name = 'fitness_app/logs.html'
    context_object_name = 'logs'
    ordering = ['workout_date']

    def get_queryset(self):
        logs = StrengthWorkout.objects.filter(username=self.request.user)
        return logs


@method_decorator(login_required, name='dispatch')
class LoggerUpdate(UpdateView):
    model = StrengthWorkout
    fields = ['workout_name', 'workout_date', 'sets', 'reps', 'workout_weight']
    template_name = 'fitness_app/update.html'
    success_url = reverse_lazy('fitness_app:logger-list')


@method_decorator(login_required, name='dispatch')
class LoggerDelete(DeleteView):
    model = StrengthWorkout
    template_name = 'fitness_app/delete.html'
    success_url = reverse_lazy('fitness_app:logger-list')


'''
Method for calculating TDEE based on the values in the TDEE calculator form

https://steelfitusa.com/2018/10/calculate-tdee/
How to calculate your BMR using the Harris-Benedict Equation:
Men BMR = 66 + (13.7 X weight in kg) + (5 x height in cm) – (6.8 x age in yrs)

Obtain TDEE by multiplying BMR by the following values based on activity level
Sedentary (little to no exercise + work a desk job) = 1.2
Lightly Active (light exercise 1-3 days / week) = 1.375
Moderately Active (moderate exercise 3-5 days / week) = 1.55
Very Active (heavy exercise 6-7 days / week) = 1.725
Extremely Active (very heavy exercise, hard labor job, training 2x / day) = 1.9
'''


def TDEEcalculation(a, h, w, x):
    BMR = 66 + 13.7 * w + 5 * h - 6.8 * a
    activity_multiplier = ""
    if x == '0':
        activity_multiplier = 1.2
    elif x == '1':
        activity_multiplier = 1.375
    elif x == '2':
        activity_multiplier = 1.55
    elif x == '3':
        activity_multiplier = 1.725

    TDEE = round((BMR * activity_multiplier), 2)
    return [TDEE, TDEE - 500, TDEE + 500]


# Generate the Ideal Caloric Intake (TDEE) Calculator Page
# This page does not need logging in.
def calculateTDEE(request):
    # get the current user as an object
    current_user = request.user

    # find the logged-in user's bodyweight
    w = 60
    if current_user.is_authenticated:
        weights = StatsOverTime.objects.filter(username=current_user).order_by('-date')
        if len(weights) > 0:
            w = weights[0].bodyweight

    # get the logged-in user's age
    age = 10
    if current_user.is_authenticated:
        dob = current_user.userstats.DOB
        now = datetime.date.today()
        age = int((now - dob).days / 365.25)

    # get the logged in user's heigh
    h = 150
    if current_user.is_authenticated:
        h = current_user.userstats.height

    # if the request method is post, retrieve the values in the calculator form and calculate ther
    # user's TDEE (total daily energy expenditure) to estimate their ideal caloric intake
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = CalculatorForm(request.POST)
        # check whether it's valid
        # then retrieve the values from the form
        if form.is_valid():
            age = form.cleaned_data['age']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            activity = form.cleaned_data['activity']
            # calculate TDEE based on the inputs above
            TDEE = TDEEcalculation(age, height, weight, activity)

            # send the TDEE values: maintenance calories, cuttting calories and bulking calories as a dictionary object
            # with an HTTP response when rendering the calc_info page. Calc_info.html will display the user's ideal
            # caloric intakes depending on their goals of maintaining, cutting or gaining weight.
            return render(request, "fitness_app/calc_info.html",
                          {'form': form, 'm_cal': TDEE[0], 'c_cal': TDEE[1], 'b_cal': TDEE[2]})


    # if a GET (or any other method) we'll create a calculator form
    # the default values in the form are the logged-in user's height, age and weight.
    # this allows the user to not have to input everything every time they use the form.
    else:
        form = CalculatorForm(initial={'height': h, 'age': age, 'weight': w})

    return render(request, 'fitness_app/calc.html', {'form': form})


# Helper functions for stats
#uses class based views so that the django default listview,updateview,deleteview could be utilised for
#displaying the stats and allowing the user to update or delete them
#method_decorator(login_required, name='dispatch') checks if the user is logged in or not.
@method_decorator(login_required, name='dispatch')
class Stats(ListView):
    model = StatsOverTime
    template_name = 'fitness_app/stats.html'
    context_object_name = 'stats'
    ordering = ['date']

    def get_queryset(self):
        stats = StatsOverTime.objects.filter(username=self.request.user)
        return stats


@method_decorator(login_required, name='dispatch')
class StatsUpdate(UpdateView):
    model = StatsOverTime
    fields = ['date', 'bodyweight', 'fat', 'calorie_intake']
    template_name = 'fitness_app/statsupdate.html'
    success_url = reverse_lazy('fitness_app:stats')


@method_decorator(login_required, name='dispatch')
class StatsDelete(DeleteView):
    model = StatsOverTime
    template_name = 'fitness_app/statsdelete.html'
    success_url = reverse_lazy('fitness_app:stats')


# This is the RESTapi function for getting the workout type as a list
class PostListViewForWorkoutType(generics.ListAPIView):
    queryset = WorkoutType.objects.all()
    serializer_class = serializers.PostSerializer
