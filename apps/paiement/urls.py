from django.urls import path
from .views import PanierView , RemoveFromCartView ,UpdateCartView , CommandeView , ConfirmationCommandeView,PaymentView,UpdateOrderStatusView,HistoryClientCommandeView,HistoryClientCommandeDetailsView,HistoryClientCommandeBackView



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
        CommandeView.as_view(template_name="commande.html"),
        name="commande",
    ),

    path(
        "add-commande/",
        CommandeView.as_view(template_name="commande.html"),
        name="add-commande",
    ),
      path(
        "confirmation-commande/<int:order_id>/",
        ConfirmationCommandeView.as_view(template_name="confirmationCommande.html"),
        name="confirmation-commande",
    ),
    path(
        "payment/<int:order_id>/",
        PaymentView.as_view(template_name="paiement.html"),
        name="payment",
    ),
    path(
        "update-statusPayment/", 
        UpdateOrderStatusView.as_view(), 
        name='update-statusPayment'),

    path(
        "history-commandesClient/", 
        HistoryClientCommandeView.as_view(template_name="commandes_client.html"), 
        name='history-commandesClient'),    

    path(
        "history-commandesClient/<int:order_id>/",
        HistoryClientCommandeDetailsView.as_view(template_name="commande_details.html"),
        name="commandeDetails",
    ),    

     path(
        "history-commandesClientBack/", 
        HistoryClientCommandeBackView.as_view(template_name="commandes_client.html"), 
        name='history-commandesClientBack'),   

       
]
