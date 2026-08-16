from django.conf import settings
from django.db import models


class OIDCProfile(models.Model):
    """Guarda los claims que envió el IdP la primera vez que el usuario
    inició sesión. En logins posteriores no se modifican."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="oidc_profile"
    )
    claims = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil OIDC de {self.user}"
