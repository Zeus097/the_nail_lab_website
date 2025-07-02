from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Търси по име и описание...',
                'class': 'search-input',
                'style': 'width: 100%;',
                'autofocus': 'autofocus',
            },
        )
    )