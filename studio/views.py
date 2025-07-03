from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView


# Create your views here.


def home_page(request):
    return render(request, 'common/base.html')


class HomePageView(TemplateView):
    success_url = reverse_lazy('home-page')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['common/base.html']
        return ['common/home-no-profile.html']
