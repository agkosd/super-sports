from django.urls import path

from . import views
from django.urls import include


# urls.py contains all of the path for views methods with the corresponding url paths.
app_name = 'fitness_app'
urlpatterns = [
    path('', views.Home, name='home'),
    path('StrengthStandards/', views.StrengthStandards, name="strengthstandards"),
    path('profile/', views.Profile, name="profile"),
    path('EditProfile/', views.editProfile, name="editprofile"),
    path('EditUser/', views.editUser, name="edituser"),
    path('SignUp/', views.SignUp, name="createprofile"),
    path('calc/', views.calculateTDEE, name="Calculator"),
    path('logger/', views.Logger, name="logger"),
    path('SignUp/info/', views.SignUpinfo, name='SignUpinfo'),
    # Paths for logger
    path('logger/list/', views.LoggerList.as_view(), name='logger-list'),
    path('logger/list/<int:pk>/update/', views.LoggerUpdate.as_view(), name='logger-update'),
    path('logger/list/<int:pk>/delete/', views.LoggerDelete.as_view(), name='logger-delete'),
    # Paths for stats over time
    path('statsovertime/', views.Statsovertime, name='statsovertime'),
    path('statsovertime/stats/',views.Stats.as_view(),name='stats'),
    path('statsovertime/stats/<int:pk>/update/',views.StatsUpdate.as_view(), name='stats-update'),
    path('statsovertime/stats/<int:pk>/delete/', views.StatsDelete.as_view(), name='stats-delete'),
    path('editgoals/', views.EditGoals, name="editgoals"),
    # API and AJAX paths
    path('api/', views.PostListViewForWorkoutType.as_view(), name='api'),
    path('ajax/check_username', views.ValidateUsername, name='check_username')

]
