from django.urls import path,include
from .views import signup_view
from .views import UserLoginView
from .views import history_view
from . import views
from .views import home 


urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('history/', history_view, name='history'),
    path('', views.home, name='home'),  # or whatever your app is called
    path('dashboard/', views.dashboard_view, name='dashboard'),
     path('', home, name='home'),

]
