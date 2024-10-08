from django.urls import path
from .views import FrontView



urlpatterns = [
    path(
        "",
      FrontView.as_view(template_name="landing.html"),
        name="landing",
    )
]
