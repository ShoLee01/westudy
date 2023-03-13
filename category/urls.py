"""
URL mapping for the user API.
"""
from django.urls import path

from category import views

app_name = "category"

urlpatterns = [
    path("create/", views.CategoryCreateView.as_view(), name="create"),
    path("", views.CategoryListView.as_view(), name="all"),
    path("<int:id>/", views.CategoryDetailView.as_view(), name="detail"),
    path("update/<int:id>/", views.CategoryUpdateView.as_view(), name="update"),
    path("delete/<int:id>/", views.CategoryDeleteView.as_view(), name="delete"),
]
