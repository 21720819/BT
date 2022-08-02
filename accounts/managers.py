from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, username, password,**extra_fields):
        if not email :
            raise ValueError('The given email mist be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save (using = self._db)
        return user

    def create_user(self, email,username, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email,username, password,**extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, username,password, **extra_fields)
