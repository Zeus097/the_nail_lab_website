from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

UserModel = get_user_model()


class BaseUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Потребителско име'),
            'email': _('Имейл'),
            'password1': _('Парола'),
            'password2': _('Потвърди паролата'),
        }

        help_texts = {
            'username': _('Позволени са букви, цифри и @/./+/-/_ само.'),
            'email': _('Въведи валиден имейл адрес.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': _('Въведи потребителско име'),
            'autofocus': True,
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': _('Въведи имейл адрес'),
        })

        self.fields['password1'].widget.attrs.update({
            'placeholder': _('Създай парола'),
        })

        self.fields['password2'].widget.attrs.update({
            'placeholder': _('Потвърди паролата'),
        })


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'placeholder': _('Потребителско име или имейл..'),
            'autofocus': True,
        })

        self.fields['password'].widget.attrs.update({
            'placeholder': _('Парола'),
        })



