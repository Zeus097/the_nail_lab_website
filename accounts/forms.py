from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from accounts.models import BaseUser
from accounts.validators import PhoneValidator

UserModel = get_user_model()


class BaseUserCreationForm(UserCreationForm):
    telephone_number = forms.CharField(
        max_length=20,
        required=True,
        label=_('Телефонен номер'),
        validators=[PhoneValidator()],
        widget=forms.TextInput(attrs={'placeholder': _('Въведи телефонен номер')})
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('username', 'email', 'telephone_number', 'password1', 'password2')
        labels = {
            'username': _('Потребителско име'),
            'email': _('Имейл'),
            'password1': _('Парола'),
            'password2': _('Потвърди паролата'),
            'telephone_number': _('Телефонен номер'),
        }
        help_texts = {
            'username': _('Позволени са букви, цифри и @/./+/-/_ само.'),
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


class ProfileEditForm(forms.ModelForm):
    # Biography is defined like that,
    # because is not from BaseUser

    biography = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 10, 'cols': 40, 'maxlength': 500,
                'placeholder': 'Максимален брой символи - 500',
                'style': 'padding: 10px;'
            }
        ),
        required=False,
        label='Биография'
    )

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'telephone_number']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': _('Потребителско име')})
        self.fields['email'].widget.attrs.update({'placeholder': _('Имейл')})
        self.fields['telephone_number'].widget.attrs.update({'placeholder': _('Телефон')})

        if user and user.is_employee:
            self.fields['biography'].initial = getattr(user.employeebio, 'biography', '')

    def save(self, commit=True):
        # Save the logic for biography for the EmployeeBio
        # if the user is employee.

        user = super().save(commit=commit)

        if user.is_employee:
            biography = self.cleaned_data.get('biography', '')
            employee_bio = user.employeebio
            employee_bio.biography = biography
            if commit:
                employee_bio.save()

        return user


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


class CompleteProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Парола")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True, label="Потвърди паролата")

    class Meta:
        model = BaseUser
        fields = ['email', 'telephone_number']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if BaseUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Този имейл вече е зает.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        pw1 = cleaned_data.get('password')
        pw2 = cleaned_data.get('password2')
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Паролите не съвпадат.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['photo']
        labels = {
            'photo': 'Снимка',
        }
