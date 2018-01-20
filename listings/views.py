from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from .models import Listing, Category
from .forms import ListingForm, SpecForm

def index(request):
    category_list = Category.objects.filter(active=True)

    return render(request, 'listing/index.html', context={
        'category_list': category_list
    })


class ListingList(View):
    form_class = ListingForm
    template = 'listing/list.html'

    def populate_category_data(self, data, category_id):
        data['category'] = get_object_or_404(Category, id=category_id, active=True)

    def populate_listing_list_data(self, data, category):
        listing_list = Listing.objects.filter(category=category)
        data['listing_public_list'] = listing_list.filter(public=True)
        data['listing_private_list'] = listing_list.filter(public=False)

    def populate_form_data(self, data, *args, **kwargs):
        data['form'] = self.form_class(*args, **kwargs)

    def get(self, request, **kwargs):
        data = {}
        populate_nav_data(data)
        self.populate_category_data(data, kwargs['category_id'])
        self.populate_listing_list_data(data, data['category'])
        self.populate_form_data(data, initial={})
        return render(request, self.template, data)

    def post(self, request, **kwargs):
        data = {}
        self.populate_form_data(data, self.request.POST, self.request.FILES)
        if data['form'].is_valid():
            data['form'].save()
            return HttpResponseRedirect(request.path_info)

        populate_nav_data(data)
        self.populate_category_data(data, kwargs['category_id'])
        self.populate_listing_list_data(data, data['category'])
        return render(request, self.template, data)


class ListingDetail(View):
    listing_form_class = ListingForm
    spec_form_class = SpecForm
    template = 'listing/detail.html'

    def populate_listing_data(self, data, listing_id):
        data['listing'] = get_object_or_404(Listing, id=listing_id, active=True)

    def populate_spec_data(self, data, listing):
        if hasattr(listing, 'spec'):
            data['spec'] = listing.spec
        else:
            data['spec'] = None

    def populate_listing_form_data(self, data, *args, **kwargs):
        data['form'] = self.listing_form_class(*args, **kwargs)

    def populate_spec_form_data(self, data, spec, *args):
        if spec:
            data['spec_form'] = self.spec_form_class(instance=spec, *args)
        else:
            data['spec_form'] = self.spec_form_class(initial={}, *args)

    def get(self, request, **kwargs):
        data = {}
        populate_nav_data(data)
        self.populate_listing_data(data, kwargs['listing_id'])
        self.populate_spec_data(data, data['listing'])
        self.populate_listing_form_data(data, instance=data['listing'])
        self.populate_spec_form_data(data, data['spec'])
        return render(request, self.template, data)

    def post(self, request, **kwargs):
        submit_type = self.request.POST.get('submit-type')
        data = {}
        self.populate_listing_data(data, kwargs['listing_id'])
        self.populate_spec_data(data, data['listing'])

        if submit_type == 'put-listing':
            self.populate_listing_form_data(data, self.request.POST, self.request.FILES, instance=data['listing'])
            if data['form'].is_valid():
                data['form'].save()
                return HttpResponseRedirect(request.path_info)
            self.populate_spec_form_data(data, data['spec'])
            self.populate_listing_data(data, kwargs['listing_id'])

        elif submit_type == 'post-or-put-spec':
            self.populate_spec_form_data(data, data['spec'], self.request.POST)
            if data['spec_form'].is_valid():
                spec = data['spec_form'].save()
                spec.listing = data['listing']
                spec.save()
                return HttpResponseRedirect(request.path_info)
            self.populate_listing_form_data(data, instance=data['listing'])

        populate_nav_data(data)
        return render(request, self.template, data)


def populate_nav_data(data):
    data['category_list'] = Category.objects.filter(active=True)
