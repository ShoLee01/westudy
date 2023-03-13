"""
URL mapping for the user API.
"""
from django.urls import path

from typeofprogram import views

app_name = "TypeOfProgram"

urlpatterns = [
    path("create/", views.TypeOfProgramCreateView.as_view(), name="create"),
    path("", views.TypeOfProgramListView.as_view(), name="all"),
    path("<int:id>/", views.TypeOfProgramDetailView.as_view(), name="detail"),
    path("update/<int:id>/", views.TypeOfProgramUpdateView.as_view(), name="update"),
    path("delete/<int:id>/", views.TypeOfProgramDeleteView.as_view(), name="delete"),
    path("preferences/<str:name>/", views.PreferredByUsersView.as_view(), name="consultation"),
]
