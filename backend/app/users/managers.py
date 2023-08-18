from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager with email as the unique identifier
    for authentication and authorization instead of username.
    """

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Missing required email address")
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        return self.create_user(email, password, **extra_fields)
