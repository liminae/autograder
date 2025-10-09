from django.urls import path

from . import views

app_name = "problems"

urlpatterns = [
    path("", views.problemset_view, name="problemset"),
    path("<int:pid>/", views.problem_view, name="problem"),
]
