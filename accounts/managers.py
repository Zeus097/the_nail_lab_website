from django.contrib.auth.base_user import BaseUserManager


class BaseUserManager(BaseUserManager):
    def create_user(self, username, email, telephone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Email е задължителен")
        if not username:
            raise ValueError("Потребителското име е задължително")
        if not telephone_number:
            raise ValueError("Телефонният номер е задължителен")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            telephone_number=telephone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, telephone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Админът трябва да има парола.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Админът трябва да има is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Админът трябва да има is_superuser=True.")

        return self.create_user(
            username=username,
            email=email,
            telephone_number=telephone_number,
            password=password,
            **extra_fields
        )
