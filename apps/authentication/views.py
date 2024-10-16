from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from .forms import LoginForm , RegisterForm;
from apps.paiement.models import Product , Cart , CartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm , BrandRequestForm
from django.contrib import messages  # For showing messages
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import User  # Ensure you import your User model



"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""

class BrandRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        brand_form = BrandRequestForm(request.POST, request.FILES, instance=request.user)
        if brand_form.is_valid():
            brand_request = brand_form.save(commit=False)
            brand_request.request_status = 'pending'  # Set the status to pending
            brand_request.save()

            # Notify the admin (you can customize this)
            messages.success(request, "Your request to become a vendor has been sent!")
            # Optional: Notify admin through email or another method

            return redirect('account-settings')  # Redirect back to the profile settings
        else:
            messages.error(request, "Please correct the errors below.")

        # If the form is invalid, return to the profile settings with errors
        return redirect('account-settings')  # You may want to return the user to the form

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account_settings.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user  # Pass the authenticated user to the template
        context['form'] = ProfileUpdateForm(instance=self.request.user)  # Include the profile form
        context['layout_path'] = TemplateHelper.set_layout("layout_user.html", context)
        return context

    def post(self, request, *args, **kwargs):
        if 'brand_request' in request.POST:
         return BrandRequestView.as_view()(request, *args, **kwargs)  # Handle brand request

        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # You can also add a success message here
            return redirect('account-settings')  # Redirect to the profile page after successful update
        context = self.get_context_data(**kwargs)
        context['form'] = form  # Include the form with errors if the update fails
        return self.render_to_response(context)




class AuthView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        login_form = LoginForm()
        # Update the context
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
                if user.role == 'ADMIN':
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
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        register_form = RegisterForm()
        # Update the context
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
            if user.role == 'ADMIN':
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
    template_name = 'vendor_requests.html'  # Template to display vendor requests
    context_object_name = 'vendor_requests'  # Context variable to access vendor requests

    def get_queryset(self):
        # Filter to get only users with pending vendor requests
        return User.objects.filter( request_status='pending')  # Adjust your filter based on your model

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context


class AcceptVendorRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.role = 'VENDEUR'  # Change the role to 'VENDEUR'
        user.request_status = 'accepted'  # Update request status
        user.save()
        messages.success(request, f"The request from {user.username} has been accepted!")
        return redirect('vendor-requests')  # Redirect to the vendor requests list

    def get_context_data(self, **kwargs):
        # You may want to add context data if necessary, for the admin layout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context


class RejectVendorRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.request_status = 'rejected'  # Update request status to rejected
        user.save()
        messages.warning(request, f"The request from {user.username} has been rejected!")
        return redirect('vendor-requests')  # Redirect to the vendor requests list

    def get_context_data(self, **kwargs):
        # You may want to add context data if necessary, for the admin layout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['layout_path'] = TemplateHelper.set_layout("layout_vertical.html", context)
        return context
