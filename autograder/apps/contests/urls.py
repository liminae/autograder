from django.urls import path

from . import views

app_name = "contests"

urlpatterns = [
    path("", views.contests_view, name="contests"),
    path("<int:cid>/", views.contest_view, name="contest"),
    path("<int:cid>/standings/", views.contest_standings_view, name="standings"),
    path(
        "<int:cid>/status/<str:mine_only>/<int:page>/",
        views.contest_status_view,
        name="status",
    ),
    path(
        "skip/<int:sid>/<int:cid>/<str:mine_only>/<int:page>/",
        views.contest_skip_view,
        name="skip",
    ),
]
