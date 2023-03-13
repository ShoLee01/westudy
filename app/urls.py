"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [   
    path("admin/", admin.site.urls),
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="api-schema"
    ),  # genera el esquema de la API
    #api/docs/
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("user/", include("user.urls"), name="user"),
    path("university/", include("university.urls"), name="university"),
    path("course/", include("course.urls"), name="course"),
    path("category/", include("category.urls"), name="category"),
    path("modality/", include("modality.urls"), name="modality"),
    path("type-of-program/", include("typeofprogram.urls"), name="typeofprogram"),
    path("schedule/", include("schedule.urls"), name="schedule"),
]
