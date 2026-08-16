from django.core.exceptions import SuspiciousOperation
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from accounts.models import OIDCProfile


class EmailOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def filter_users_by_claims(self, claims):
        email = claims.get("email")
        if not email:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(email__iexact=email)

    def get_username(self, claims):
        email = claims.get("email")
        if not email:
            raise SuspiciousOperation(
                'No llegó "email"... ¿por qué?'
            )
        return email

    def create_user(self, claims):
        email = claims.get("email")
        user = self.UserModel.objects.create_user(username=email, email=email)
        user.first_name = claims.get("given_name", "") or ""
        user.last_name = claims.get("family_name", "") or ""
        user.save()
        OIDCProfile.objects.create(user=user, claims=claims)
        self._remember_claims_for_display(new_claims=claims, stored_claims=None, first_login=True)
        return user

    def update_user(self, user, claims):
        # El usuario ya existía: se ignoran los datos nuevos del IdP para no
        # sobreescribir lo guardado, pero se muestran ambos en la página de
        # éxito (los guardados y los que acaban de llegar).
        profile = getattr(user, "oidc_profile", None)
        if profile is None:
            # No había datos guardados (p. ej. el usuario se creó fuera del
            # flujo OIDC): se guardan ahora, como si fuera su primer login.
            OIDCProfile.objects.create(user=user, claims=claims)
            self._remember_claims_for_display(new_claims=claims, stored_claims=None, first_login=True)
            return user

        self._remember_claims_for_display(
            new_claims=claims, stored_claims=profile.claims, first_login=False
        )
        return user

    def _remember_claims_for_display(self, new_claims, stored_claims, first_login):
        if getattr(self, "request", None) is not None:
            self.request.session["oidc_claims_new"] = new_claims
            self.request.session["oidc_claims_stored"] = stored_claims
            self.request.session["oidc_first_login"] = first_login
