from django.urls import path

from .views import ContactCreateView, IndexView, ProjectDetailView

app_name = "portfolio"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact/", ContactCreateView.as_view(), name="contact"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail"),
]
