from django import forms
from photos.models import GalleryPhoto, CertificateImage


class GalleryBaseForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ['name', 'description', 'photo']
        labels = {
            'name': 'Заглавие',
            'description': 'Описание',
            'photo': 'Снимка'
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 10,

                'placeholder': 'Описание'
            }),
        }


class CertificateBaseForm(forms.ModelForm):
    class Meta:
        model = CertificateImage
        fields = ['photo']
        labels = {
            'photo': 'Снимка'
        }
