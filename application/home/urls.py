from django.urls import path
from . views import *

urlpatterns = [
    path('health/', health),
    path('health/startup/', startup),
    path('health/ready/', readiness),
    path('health/live/', liveness),

    path('', home, name = 'home'),

    path('register/', register, name = 'register'),
    path('login/', login, name = 'login'),
    path('logout/', logout, name = 'logout'),
]