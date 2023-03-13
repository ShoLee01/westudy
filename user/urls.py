"""
URL mapping for the user API.
"""
from django.urls import path

from user import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("user/", views.ManageUserView.as_view(), name="user"),
    path("login/", views.Login.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("registered-users/", views.ManageUserListView.as_view(), name="users"),
    path("delete/", views.ManageDeleteView.as_view(), name="delete"),
    path("saved-courses/<int:id>/", views.CreateFavoriteCourseView.as_view(), name="course"),
    path("course/unsubscribe/<int:id>/", views.DeleteFavoriteCourseView.as_view(), name="course-delete"),
    path("my-courses/", views.ManageViewOfCoursesAssociatedUser.as_view(), name="courses"),
    path("program/subscribed/<int:id>/", views.ProgramPreferenceView.as_view(), name="program"),
]
