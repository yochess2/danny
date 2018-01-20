from django.conf import settings
from django.views import View
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from .models import Profile
from .forms import AboutDaniel
from listings.models import Category

ADMIN = settings.ADMIN

class AboutDaniel(View):
    template = 'userprofile/aboutdaniel.html'
    form_class = AboutDaniel

    def populate_profile_data(self, data):
        data['admin'] = get_object_or_404(Profile, user__username=ADMIN)

    def populate_form_data(self, data, *args, **kwargs):
        data['form'] = self.form_class(*args, **kwargs)

    def get(self, request, **kwargs):
        data = {}
        populate_nav_data(data)
        self.populate_profile_data(data)
        self.populate_form_data(data, instance=data['admin'])
        return render(request, self.template, data)

    def post(self, request, **kwargs):
        data = {}
        populate_nav_data(data)
        self.populate_profile_data(data)
        self.populate_form_data(data, self.request.POST, self.request.FILES, instance=data['admin'])
        if data['form'].is_valid():
            data['form'].save()
            return HttpResponseRedirect(request.path_info)
        return render(request, self.template, data)

def populate_nav_data(data):
    data['category_list'] = Category.objects.filter(active=True)
