from django.urls import path
from .views import PanierView , RemoveFromCartView ,UpdateCartView , PaymentView



urlpatterns = [
    path(
        "products",
        PanierView.as_view(template_name="products.html"),
        name="products",
    ),

    path(
        "panier",
        PanierView.as_view(template_name="panier.html"),
        name="panier",
    ),

    path(
        "remove-from-cart/", 
         RemoveFromCartView.as_view(), 
         name='remove_from_cart'
    ),

    path(
        "update-cart/", 
        UpdateCartView.as_view(), 
        name='update_cart'),
  
      path(
        "commande/",
        PaymentView.as_view(template_name="commande.html"),
        name="commande",
    ),
]
