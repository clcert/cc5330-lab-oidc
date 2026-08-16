from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView


def home(request):
    return render(request, "accounts/home.html")


@login_required
def success(request):
    context = {
        "new_claims": request.session.get("oidc_claims_new", {}),
        "stored_claims": request.session.get("oidc_claims_stored"),
        "first_login": request.session.get("oidc_first_login", False),
    }
    return render(request, "accounts/success.html", context)


def error(request):
    message = request.session.pop("oidc_error", None)
    return render(request, "accounts/error.html", {"message": message})


class CustomOIDCCallbackView(OIDCAuthenticationCallbackView):
    @property
    def failure_url(self):
        return "/error/"

    def get(self, request):
        if request.GET.get("error"):
            request.session["oidc_error"] = (
                request.GET.get("error_description") or request.GET.get("error")
            )

        response = super().get(request)

        if (
            isinstance(response, HttpResponseRedirect)
            and response.url == self.failure_url
        ):
            request.session.setdefault(
                "oidc_error",
                "Algo falló... ¿por qué?",
            )

        return response
