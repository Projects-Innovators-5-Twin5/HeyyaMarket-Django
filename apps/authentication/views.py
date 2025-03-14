from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from .forms import LoginForm , RegisterForm;
from .forms import UserForm
from apps.paiement.models import Product , Cart , CartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm , BrandRequestForm
from django.contrib import messages 
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import User 



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""






class AuthView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        login_form = LoginForm()
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                "login_form": login_form,
            }
        )

        return context


    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'ADMIN' or user.role == 'VENDEUR':
                  return redirect('index')
                else:
                   return redirect('landing')
            else:
                form.add_error(None, "Email ou mot de passe incorrect.")

        context = self.get_context_data(**kwargs)
        context['login_form'] = form
        return self.render_to_response(context)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('auth-login-basic')



class RegisterView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        register_form = RegisterForm()
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                'register_form':register_form
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            if user.role == 'ADMIN' or user.role == 'VENDEUR':
                return redirect('index')
            else:
                return redirect('landing')
        else:
            print(register_form.errors)
            context = self.get_context_data(**kwargs)
            context['register_form'] = register_form
            return self.render_to_response(context)


class VendorRequestsView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'vendor_requests.html'  
    context_object_name = 'vendor_requests'  

    def get_queryset(self):
        return User.objects.filter( request_status='pending') 

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context


class AcceptVendorRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.role = 'VENDEUR'  
        user.request_status = 'accepted'  
        user.save()
        messages.success(request, f"The request from {user.username} has been accepted!")
        return redirect('vendor-requests') 

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context


class RejectVendorRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.request_status = 'rejected'  
        user.save()
        messages.warning(request, f"The request from {user.username} has been rejected!")
        return redirect('vendor-requests')  

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context

class ListeUserView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'user_list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        login_form = LoginForm()
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            }
        )

        return context


    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'ADMIN' or user.role == 'VENDEUR':
                  return redirect('index')
                else:
                   return redirect('landing')
            else:
                form.add_error(None, "Email ou mot de passe incorrect.")

        context = self.get_context_data(**kwargs)
        context['login_form'] = form
        return self.render_to_response(context)



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('auth-login-basic')



class RegisterView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        register_form = RegisterForm()
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                'register_form':register_form
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            if user.role == 'ADMIN' or user.role == 'VENDEUR':
                return redirect('index')
            else:
                return redirect('landing')
        else:
            print(register_form.errors)
            context = self.get_context_data(**kwargs)
            context['register_form'] = register_form
            return self.render_to_response(context)



class BrandRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        brand_form = BrandRequestForm(request.POST, request.FILES, instance=request.user)
        if brand_form.is_valid():
            brand_request = brand_form.save(commit=False)
            brand_request.request_status = 'pending' 
            brand_request.save()

            messages.success(request, "Your request to become a vendor has been sent!")

            return redirect('account-settings')  
        else:
            messages.error(request, "Please correct the errors below.")

        return redirect('account-settings') 
    
    

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account_settings.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user 
        context['form'] = ProfileUpdateForm(instance=self.request.user)  
        context['layout_path'] = TemplateHelper.set_layout("layout_user.html", context)
        return context

    def post(self, request, *args, **kwargs):
        if 'brand_request' in request.POST:
         return BrandRequestView.as_view()(request, *args, **kwargs) 

        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account-settings')  
        context = self.get_context_data(**kwargs)
        context['form'] = form  
        return self.render_to_response(context)
    


class VendorRequestsView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'vendor_requests.html' 
    context_object_name = 'vendor_requests'  

    def get_queryset(self):
        return User.objects.filter( request_status='pending')  

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context


class AcceptVendorRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.role = 'VENDEUR' 
        user.request_status = 'accepted' 
        user.save()
        messages.success(request, f"The request from {user.username} has been accepted!")
        return redirect('vendor-requests')  

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context


class RejectVendorRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.request_status = 'rejected'
        user.save()
        messages.warning(request, f"The request from {user.username} has been rejected!")
        return redirect('vendor-requests')  

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context
class ModifierUserView(View):
    def get_object(self, user_id):
        return get_object_or_404(User, id=user_id)

    def post(self, request, user_id):
        user = self.get_object(user_id)

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.tel = request.POST.get('tel')
        user.addresse = request.POST.get('addresse')
        user.bio = request.POST.get('bio')
        user.role = request.POST.get('role')

        user.save()  

        messages.success(request, 'Utilisateur mis à jour avec succès.')
        return  redirect('user_list')
    

class SupprimerUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        user.delete()

        return  redirect('user_list')
