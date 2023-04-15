"""
URL mapping for the user API.
"""
from django.urls import path

from schedule import views

app_name = "schedule"

urlpatterns = [
    path('create/course/<int:id>/', views.ScheduleCreateView.as_view(), name='create'),
    path('', views.ScheduleListView.as_view(), name='list'),
    path('<int:id>/', views.ScheduleGetView.as_view(), name='get'),
    path('update/<int:id>/', views.ScheduleUpdateView.as_view(), name='update'),
    path('delete/<int:id>/', views.ScheduleDeleteView.as_view(), name='delete'),
    path('course/<int:id>/', views.ScheduleListCourseView.as_view(), name='course'),
]
