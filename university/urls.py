"""
URL mapping for the user API.
"""
from django.urls import path

from university import views

app_name = "university"

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("<int:id>", views.UniversityGetView.as_view(), name="get"),
    path("detail/<int:id>", views.UniversityGetLoginView.as_view(), name="get"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", views.UniversityListView.as_view(), name="list"),
    path("create/", views.UniversityCreateView.as_view(), name="create"),
    path("update/<int:id>", views.UniversityUpdateView.as_view(), name="update"),
    path("delete/<int:id>", views.UniversityDeleteView.as_view(), name="delete"),
    path('active/', views.UniversityActivateView.as_view(), name='active_universities'),
    path('inactive/', views.InactiveUniversitiesView.as_view(), name='inactive_universities'),
    
]
