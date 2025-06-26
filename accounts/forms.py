from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'autofocus': True,
        })

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Потребителско име или имейл..',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Парола',
        })



