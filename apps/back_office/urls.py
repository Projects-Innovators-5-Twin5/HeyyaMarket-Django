from django.urls import path
from .views import BackView



urlpatterns = [
    path(
        "",
      BackView.as_view(template_name="analytics.html"),
        name="analytics",
    )
]
