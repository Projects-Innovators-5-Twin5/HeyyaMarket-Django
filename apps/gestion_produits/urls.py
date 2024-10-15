

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('categories/', views.CategoryView.as_view(), name='categorie_list'),
    path('categorie/<int:pk>/', views.CategoryDetailView.as_view(), name='categorie_detail'),
    path('categorie/ajouter/', views.CategoryCreateView.as_view(), name='categorie_add'),
    path('categories/<int:pk>/modifier/', views.CategoryUpdateView.as_view(), name='categorie_edit'),
    path('categorie/<int:pk>/supprimer/', views.CategoryDeleteView.as_view(), name='categorie_delete'),

    path('produits/', views.ProductView.as_view(), name='product_list'),
    path('front/produits/', views.ProductFrontView.as_view(), name='product_front'),
    path('produit/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('back/produit/<int:pk>/', views.ProductDetailBackView.as_view(), name='product_detail_back'),
    path('produit/ajouter/', views.ProductCreateView.as_view(), name='product_add'),
    path('produit/<int:pk>/modifier/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('produit/<int:pk>/supprimer/', views.ProductDeleteView.as_view(), name='product_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)