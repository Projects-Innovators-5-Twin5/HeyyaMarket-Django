from django.urls import path
from .views import AuthView , LogoutView , RegisterView , ProfileView , VendorRequestsView, AcceptVendorRequestView, RejectVendorRequestView


urlpatterns = [
    path(
        "auth/login/",
        AuthView.as_view(template_name="auth_login_basic.html"),
        name="auth-login-basic",
    ),
    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="auth-logout",
    ),
    path(
        "auth/register/",
        RegisterView.as_view(template_name="auth_register_basic.html"),
        name="auth-register-basic",
    ),
    path(
        "auth/forgot_password/",
        AuthView.as_view(template_name="auth_forgot_password_basic.html"),
        name="auth-forgot-password-basic",
    ),
    path('request-become-vendeur/', ProfileView.as_view(), name='send_brand_request'),


        path("account/settings/", ProfileView.as_view(), name="account-settings"),  

    path('vendor-requests/', VendorRequestsView.as_view(), name='vendor-requests'),
    path('vendor-requests/accept/<int:pk>/', AcceptVendorRequestView.as_view(), name='accept-vendor-request'),
    path('vendor-requests/reject/<int:pk>/', RejectVendorRequestView.as_view(), name='reject-vendor-request'),

]
