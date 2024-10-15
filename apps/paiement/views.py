from django.conf import settings
from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from apps.gestion_produits.models import Product
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart , CartItem , Order ,OrderItem , User
from decimal import Decimal
import stripe;
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""


class PanierView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        cart_items = []
        total = 0

        if self.request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=self.request.user)
            for cart_item in user_cart.items.all():  
                cart_items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'total_price': cart_item.product.prix * cart_item.quantity
                })
                total += cart_item.product.prix * cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            print(cart)
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.prix * quantity
                })
                total += product.prix * quantity

        context['cart_items'] = cart_items
        context['total'] = total

        context.update({
            "layout_path": TemplateHelper.set_layout("layout_user.html", context),
        })

        return context
    

    def post(self, request, *args, **kwargs):
        quantity = 1
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
           add_to_cart_db(request.user, product_id ,quantity)
        else:
            cart = request.session.get('cart', {})
            
            if str(product_id) in cart:
                cart[str(product_id)] += 1  
            else:
                cart[str(product_id)] = 1  
            
            request.session['cart'] = cart

        return redirect('panier') 
    

    
def add_to_cart_db(user, product_id,quantity):
    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
    if not created:
        cart_item.quantity += quantity
    cart_item.save()

        
class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')  

        if request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=request.user)

            cart_item = user_cart.items.all().filter(product_id=product_id).first()
            if cart_item:
                cart_item.delete()
        else:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                del cart[str(product_id)]

            request.session['cart'] = cart

        return redirect('panier') 


class UpdateCartView(View):
    @csrf_exempt  
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        if request.user.is_authenticated:
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = user_cart.items.all().get_or_create(product_id=product_id)

            if int(quantity) > 0:
                cart_item.quantity = int(quantity)  
                cart_item.save()
            else:
                cart_item.delete()  

        else:
            cart = request.session.get('cart', {})

            if int(quantity) > 0:
                cart[str(product_id)] = int(quantity)  
            elif str(product_id) in cart:
                del cart[str(product_id)]  

            request.session['cart'] = cart

        return JsonResponse({'success': True, 'cart': request.session.get('cart', {})})
    


class CommandeView(TemplateView):
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        cart_items = []
        total = 0
        livraison = 7.00
        total_amount = 0

        user_cart, created = Cart.objects.get_or_create(user=self.request.user)
        for cart_item in user_cart.items.all():  
            cart_items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'total_price': cart_item.product.prix * cart_item.quantity
                })
            total += cart_item.product.prix * cart_item.quantity   
        
        total_amount = Decimal(total) + Decimal(livraison)
        context['cart_items'] = cart_items
        context['total'] = total_amount
        context['livraison'] = livraison

        context.update({
            "layout_path": TemplateHelper.set_layout("layout_user.html", context),
        })

        return context   
     
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        payment_method = request.POST.get('default-radio-1') 
        user_cart = Cart.objects.get(user=user)

        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        tel = request.POST.get('tel')

        if not user.first_name or not user.last_name or not user.email or not user.addresse or not user.tel:
            user.first_name = firstname if firstname else user.first_name
            user.last_name = lastname if lastname else user.last_name
            user.email = email if email else user.email
            user.addresse = adresse if adresse else user.addresse
            user.tel = tel if tel else user.tel
            user.save()        

        order = Order.objects.create(
            user=self.request.user,
            total_amount=self.get_context_data()['total'],
            payment_method=payment_method,
            is_paid=False
        )

        for cart_item in user_cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        for cart_item in user_cart.items.all():
            cart_item.delete()

        if(payment_method == 'livraison'):
           subject = "Confirmation de votre commande"
           html_message = render_to_string('emails/confirmation_commandeEmail.html', {'user': user, 'order': order})
           recipient_list = [user.email]

           email = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, recipient_list)
           email.attach_alternative(html_message, "text/html")
           email.send(fail_silently=False)
           return redirect('confirmation-commande', order_id=order.id)
        else:
           return redirect('payment', order_id=order.id)


class ConfirmationCommandeView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        order_id = self.kwargs.get('order_id') 

        order_items = []
        order = Order.objects.get(id=order_id)
        for order_item in order.items.all():  
            order_items.append({
                    'product': order_item.product,
                    'quantity': order_item.quantity,
                    'total_price': order_item.product.prix * order_item.quantity
                })
        context['order_items'] = order_items
        context['order'] = order

        # Update the context
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_user.html", context),
        })

        return context   
    

    
class PaymentView(TemplateView):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        order_id = self.kwargs.get('order_id') 
        order_items = []
        TND_TO_EUR_RATE = Decimal('0.30')

        order = Order.objects.get(id=order_id)
        for order_item in order.items.all():  
            order_items.append({
                    'product': order_item.product,
                    'quantity': order_item.quantity,
                    'total_price': order_item.product.prix * order_item.quantity
                })
        
        total_in_eur = order.total_amount * TND_TO_EUR_RATE
        total_amount_in_eur = int(total_in_eur * 100)

        payment_intent = stripe.PaymentIntent.create(
            amount=total_amount_in_eur,
            currency='eur',  
            payment_method_types=['card'],
        )

        context['order'] = order
        context['total'] = order.total_amount
        context['order_items'] = order_items
        context['client_secret'] = payment_intent.client_secret  

        context.update({
            "layout_path": TemplateHelper.set_layout("layout_user.html", context),
        })

        return context       
    

class UpdateOrderStatusView(View):
    @csrf_exempt  
    def post(self, request, *args, **kwargs):
        try:
            user=self.request.user
            data = json.loads(request.body)
            order_id = data.get('order_id')  
            
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.save()
            subject = "Confirmation de votre commande"
            html_message = render_to_string('emails/confirmation_commandeEmail.html', {'user': user, 'order': order})
            recipient_list = [user.email]

            email = EmailMultiAlternatives(subject, "", settings.DEFAULT_FROM_EMAIL, recipient_list)
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            
            return JsonResponse({'success': True})
        
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class HistoryClientCommandeView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        user = self.request.user
        orders = Order.objects.filter(user=user)
        
        context['orders'] = orders

        # Update the context
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_user.html", context),
        })

        return context      

class HistoryClientCommandeBackView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        orders = Order.objects.filter()
        
        context['orders'] = orders

        # Update the context
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        })

        return context         

    
class HistoryClientCommandeDetailsView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        
        order_id = self.kwargs.get('order_id') 

        order_items = []
        order = Order.objects.get(id=order_id)
        user = order.user
        print(user)
        for order_item in order.items.all():  
            order_items.append({
                    'product': order_item.product,
                    'quantity': order_item.quantity,
                    'total_price': order_item.product.prix * order_item.quantity
                })
        context['order_items'] = order_items
        context['order'] = order
        context['user'] = user

        context.update({
            "layout_path": TemplateHelper.set_layout("layout_user.html", context),
        })

        return context  
