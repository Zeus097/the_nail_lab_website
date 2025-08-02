from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy

from accounts.models import EmployeeBio
from photos.forms import GalleryBaseForm, CertificateBaseForm
from photos.models import GalleryPhoto, CertificateImage


class GalleryView(LoginRequiredMixin, ListView):
    model = GalleryPhoto
    template_name = 'photos_gallery/gallery_main.html'
    context_object_name = 'gallery_list'
    paginate_by = 8

    def get_queryset(self):
        return GalleryPhoto.objects.all().order_by('-upload_date')


class GalleryUploadView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # Uses js to visualize the photo name

    model = GalleryPhoto
    form_class = GalleryBaseForm
    template_name = 'photos_gallery/gallery_upload.html'
    success_url = reverse_lazy('gallery')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_employee

    def handle_no_permission(self):
        return redirect(reverse_lazy("gallery"))

    def form_valid(self, form):
        form.instance.uploader = EmployeeBio.objects.get(user=self.request.user)
        return super().form_valid(form)



    def form_invalid(self, form):
        print("❌ FORM INVALID:", form.errors)
        return super().form_invalid(form)








class GalleryDeleteView(LoginRequiredMixin, DeleteView):
    model = GalleryPhoto
    template_name = 'photos_gallery/gallery_delete_img.html'

    def get_success_url(self):
        return reverse_lazy("gallery")


class CertificateUploadView(LoginRequiredMixin,  CreateView):
    # Also uses js to visualize the photo name

    model = CertificateImage
    form_class = CertificateBaseForm
    template_name = 'photos_gallery/certificate_upload.html'
    success_url = reverse_lazy('contact-list')

    def form_valid(self, form):
        form.instance.uploader = self.request.user.employeebio
        return super().form_valid(form)

# ADMIN WILL DELETE CERTIFICATES!
