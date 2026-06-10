from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
    'dashboard-v2/',
    views.dashboard_v2,
    name='dashboard_v2'
),

    path(
        'dashboard-v3/',
        views.dashboard_v3,
        name='dashboard_v3'
    ),
]