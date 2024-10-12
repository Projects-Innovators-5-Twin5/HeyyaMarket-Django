from django.urls import path
from .views import PanierView , RemoveFromCartView ,UpdateCartView , PaymentView , ConfirmationCommandeView



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

    path(
        "add-commande/",
        PaymentView.as_view(template_name="commande.html"),
        name="add-commande",
    ),
      path(
        "confirmation-commande/<int:order_id>/",
        ConfirmationCommandeView.as_view(template_name="confirmationCommande.html"),
        name="confirmation-commande",
    ),
]
