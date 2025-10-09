from django.urls import path

from . import views

app_name = "problems"

urlpatterns = [
    path("login/", views.tjioi_login_view, name="login"),
]
