from django.contrib.auth.base_user import BaseUserManager

class BaseUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Всеки потребител трябва да има имейл адрес.')

        if not username:
            raise ValueError('Всеки потребител трябва да има потребителско име.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError('Администраторът трябва да има парола.')

        if not extra_fields.get('is_staff'):
            raise ValueError('Администраторът трябва да има включен is_staff=True.')

        if not extra_fields.get('is_superuser'):
            raise ValueError('Администраторът трябва да има включен is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
