from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy

from accounts.models import EmployeeBio
from photos.forms import GalleryBaseForm, CertificateBaseForm
from photos.models import GalleryPhoto, CertificateImage


class GalleryView(LoginRequiredMixin, ListView):
    model = GalleryPhoto
    template_name = 'photos_gallery/gallery-main.html'
    context_object_name = 'gallery_list'
    paginate_by = 8

    def get_queryset(self):
        return GalleryPhoto.objects.all().order_by('-upload_date')


class GalleryUploadView(LoginRequiredMixin, CreateView):
    model = GalleryPhoto
    form_class = GalleryBaseForm
    template_name = 'photos_gallery/gallery-upload.html'
    success_url = reverse_lazy('gallery')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_employee

    def form_valid(self, form):
        form.instance.uploader = EmployeeBio.objects.get(user=self.request.user)
        return super().form_valid(form)


class GalleryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GalleryPhoto
    template_name = 'photos_gallery/gallery-delete-img.html'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_employee

    def handle_no_permission(self):
        return redirect(reverse_lazy("gallery"))

    def get_success_url(self):
        return reverse_lazy("gallery")


class CertificateUploadView(LoginRequiredMixin,  UserPassesTestMixin, CreateView):
    model = CertificateImage
    form_class = CertificateBaseForm
    template_name = 'photos_gallery/certificate-upload.html'
    success_url = reverse_lazy('contact-list')

    def test_func(self):
        return hasattr(self.request.user, 'employeebio')

    def form_valid(self, form):
        form.instance.uploader = self.request.user.employeebio
        return super().form_valid(form)
