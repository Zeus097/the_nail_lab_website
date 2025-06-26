from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


UserModel = get_user_model()


class BaseUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Потребителско име',
            'email': 'Имейл',
            'password1': 'Парола',
            'password2': 'Потвърди парола',
        }

        help_texts = {
            'username': 'Позволени са букви, цифри и @/./+/-/_ само.',
            'email': 'Въведи валиден имейл адрес.',
        }





