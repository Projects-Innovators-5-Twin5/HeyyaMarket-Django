from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from .models import Product;
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Cart , CartItem

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
                    'total_price': cart_item.product.price * cart_item.quantity
                })
                total += cart_item.product.price * cart_item.quantity
        else:
            cart = self.request.session.get('cart', {})
            print(cart)
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=product_id)
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price * quantity
                })
                total += product.price * quantity

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
    

class PaymentView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        cart_items = []
        total = 0

        user_cart, created = Cart.objects.get_or_create(user=self.request.user)
        for cart_item in user_cart.items.all():  
            cart_items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'total_price': cart_item.product.price * cart_item.quantity
                })
            total += cart_item.product.price * cart_item.quantity   

        context['cart_items'] = cart_items
        context['total'] = total

        # Update the context
        context.update({
            "layout_path": TemplateHelper.set_layout("layout_user.html", context),
        })

        return context    



def add_to_cart_db(user, product_id,quantity):
    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
    if not created:
        cart_item.quantity += quantity
    cart_item.save()