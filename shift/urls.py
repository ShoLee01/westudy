from django.urls import path

from shift import views

app_name = "shift"

urlpatterns = [
    path("create/course/<int:id>/", views.ShiftCreateView.as_view(), name="create"),
    path("course/<int:id>/", views.ShiftListView.as_view(), name="all"),
    path("course/<int:id>/shifts/", views.ShiftByCourseListView.as_view(), name="shifts"),
    path("delete/<int:id>/", views.ShiftDeleteView.as_view(), name="delete"),
]
