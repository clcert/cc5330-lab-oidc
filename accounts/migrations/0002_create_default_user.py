import secrets

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_default_user(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    OIDCProfile = apps.get_model("accounts", "OIDCProfile")

    random_user = secrets.token_hex(4)
    email = f"{random_user}@hackerlab.cl"

    user = User.objects.create(
        username=email,
        email=email,
        first_name="Super",
        last_name="Admin",
        password=make_password(None), 
    )

    claims = {
        "email": email,
        "given_name": "Super",
        "family_name": "Admin",
    }
    OIDCProfile.objects.create(user=user, claims=claims)

    print(f"Usuario por defecto creado: {email}")


def remove_default_user(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_user, remove_default_user),
    ]
