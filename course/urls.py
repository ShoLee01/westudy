"""
URL mapping for the user API.
"""
from django.urls import path

from course import views

app_name = "course"

urlpatterns = [
   path("create/university/<int:id>/", views.CourseCreateView.as_view(), name="create"),
   path("university/<int:id>/", views.CourseListByUniversityView.as_view(), name="list"),
   path("", views.CourseListView.as_view(), name="all"),
   path("<int:id>/", views.CourseDetailView.as_view(), name="detail"),
   path("update/<int:id>/", views.CourseUpdateView.as_view(), name="update"),
   path("delete/<int:id>/", views.CourseDeleteView.as_view(), name="delete"),   
   # Create a relationship
   path("create/category/<int:category_id>/course/<int:course_id>/", views.CategoryAssignmentSerializer.as_view(), name="create_category"),
   path("create/modality/<int:modality_id>/course/<int:course_id>/", views.ModalityAssignmentSerializer.as_view(), name="create_modality"),
   path("create/typeofprogram/<int:type_of_program_id>/course/<int:course_id>/", views.TypeOfProgramAssignmentSerializer.as_view(), name="create_typeofprogram"),
   # Delete a relationship
   path("delete/category/<int:category_id>/course/<int:course_id>/", views.CategoryDeleteAssignmentSerializer.as_view(), name="delete_category"),
   path("delete/modality/<int:modality_id>/course/<int:course_id>/", views.ModalityDeleteAssignmentSerializer.as_view(), name="delete_modality"),
   path("delete/typeofprogram/<int:type_of_program_id>/course/<int:course_id>/", views.TypeOfProgramDeleteAssignmentSerializer.as_view(), name="delete_typeofprogram"),
   # filter
   path('filter/', views.CourseFilterView.as_view(), name='filter-courses'),
]
