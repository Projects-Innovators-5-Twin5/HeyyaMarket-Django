# produits/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URLs des Catégories
    path('categories/', views.CategoryListView.as_view(), name='categorie_list'),
    path('categorie/<int:pk>/', views.CategoryDetailView.as_view(), name='categorie_detail'),
    path('categorie/ajouter/', views.CategoryCreateView.as_view(), name='categorie_add'),
    path('categorie/<int:pk>/modifier/', views.CategoryUpdateView.as_view(), name='categorie_edit'),
    path('categorie/<int:pk>/supprimer/', views.CategoryDeleteView.as_view(), name='categorie_delete'),

    # URLs des Produits
    path('produits/', views.ProductListView.as_view(), name='product_list'),
    path('produit/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('produit/ajouter/', views.ProductCreateView.as_view(), name='product_add'),
    path('produit/<int:pk>/modifier/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('produit/<int:pk>/supprimer/', views.ProductDeleteView.as_view(), name='product_delete'),
]
