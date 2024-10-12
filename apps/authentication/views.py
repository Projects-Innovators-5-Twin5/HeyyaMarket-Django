from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from .forms import LoginForm , RegisterForm;
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "account_settings.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['user'] = self.request.user  # Pass the authenticated user to the template
        context['form'] = ProfileUpdateForm(instance=self.request.user)  # Include the profile form
        context['layout_path'] = TemplateHelper.set_layout("layout_user.html", context)
        return context

    def post(self, request, *args, **kwargs):
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
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        login_form = LoginForm()
        register_form = RegisterForm()
        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
                "login_form": login_form,
                'register_form':register_form
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