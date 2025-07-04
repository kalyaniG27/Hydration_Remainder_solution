from django.urls import path
from . import views

app_name = 'tracker' 


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
   # path('dashboard/', views.dashboard_view, name='dashboard'),
    path('history/', views.history_view, name='history'),
    path('profile/', views.profile_view, name='profile'),
    path('check_reminder_due/', views.check_reminder_due, name='check_reminder_due'),
    path('test-email/', views.test_email, name='test_email'),
    path('test-email/', views.test_email_view, name='test_email'),

  
]