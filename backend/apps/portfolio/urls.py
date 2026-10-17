from django.urls import path

from .views import IndexView, ProjectDetailView

app_name = "portfolio"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
]
