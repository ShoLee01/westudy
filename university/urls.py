"""
URL mapping for the user API.
"""
from django.urls import path

from university import views

app_name = "university"

urlpatterns = [
    path("<int:id>", views.UniversityGetView.as_view(), name="get"),
    path("", views.UniversityListView.as_view(), name="list"),
    path("create/", views.UniversityCreateView.as_view(), name="create"),
    path("update/<int:id>", views.UniversityUpdateView.as_view(), name="update"),
    path("delete/<int:id>", views.UniversityDeleteView.as_view(), name="delete"),
]
