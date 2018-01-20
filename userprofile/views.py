from django.views import View
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from listings.models import Category

class AboutDaniel(View):
    template = 'userprofile/aboutdaniel.html'

    def get(self, request, **kwargs):
        data = {}
        populate_nav_data(data)
        return render(request, self.template, data)

    def post(self, request, **kwargs):
        data = {}
        populate_nav_data(data)
        return render(request, self.template, data)

def populate_nav_data(data):
    data['category_list'] = Category.objects.filter(active=True)
