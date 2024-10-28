from django.urls import path
from .views import LandingView
from apps.gestion_produits.views import ProductLandingView  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(
        "",
      ProductLandingView.as_view(template_name="landing.html"),
        name="landing",
    )
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
