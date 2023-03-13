"""
URL mapping for the user API.
"""
from django.urls import path

from modality import views

app_name = "Modality"

urlpatterns = [
    path("create/", views.ModalityCreateView.as_view(), name="create"),
    path("", views.ModalityListView.as_view(), name="all"),
    path("<int:id>/", views.ModalityDetailView.as_view(), name="detail"),
    path("update/<int:id>/", views.ModalityUpdateView.as_view(), name="update"),
    path("delete/<int:id>/", views.ModalityDeleteView.as_view(), name="delete"),
]
