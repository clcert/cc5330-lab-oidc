from django.contrib import admin
from django.urls import path
from mozilla_django_oidc.views import OIDCAuthenticationRequestView, OIDCLogoutView

from accounts import views as accounts_views
from accounts.views import CustomOIDCCallbackView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accounts_views.home, name="home"),
    path("success/", accounts_views.success, name="success"),
    path("error/", accounts_views.error, name="error"),
    path(
        "oidc/authenticate/",
        OIDCAuthenticationRequestView.as_view(),
        name="oidc_authentication_init",
    ),
    path(
        "oidc/callback/",
        CustomOIDCCallbackView.as_view(),
        name="oidc_authentication_callback",
    ),
    path("oidc/logout/", OIDCLogoutView.as_view(), name="oidc_logout"),
]
