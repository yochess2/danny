from django.conf import settings
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied

from .models import Listing, Category
from .forms import ListingForm, SpecForm, CategoryForm

ADMIN = settings.ADMIN

def index(request):
    data = {}
    populate_nav_data(data)

    return render(request, 'listing/index.html', data)


class CategoryDetails(View):
    form_class = CategoryForm
    template = 'listing/categories.html'

    def populate_form_datas(self, data, category_set, *args, **kwargs):
        if is_admin(self.request.user):
            data['forms']  = []
            return_form = False

            for category in category_set:
                if 'category_id' in kwargs and int(kwargs['category_id']) == category.id:
                    form = self.form_class(*args, instance=category)
                    return_form = form
                else:
                    form = self.form_class(instance=category)
                category_form = {
                    'category_id': category.id,
                    'form': form
                }
                data['forms'].append(category_form)

            return return_form

    def get(self, request, **kwargs):
        if not is_admin(self.request.user):
            raise PermissionDenied
        data = {}
        populate_nav_data(data)
        category_set = Category.objects.filter(active=True)
        self.populate_form_datas(data, category_set)
        return render(request, self.template, data)

    def post(self, request, **kwargs):
        if not is_admin(self.request.user):
            raise PermissionDenied
        data = {}
        category_id = self.request.POST.get('category_id')
        title = self.request.POST.get('title')

        populate_nav_data(data)
        category_set = Category.objects.filter(active=True)
        form = self.populate_form_datas(data, category_set, {'title': title}, category_id=category_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
        return render(request, self.template, data)


class ListingList(View):
    form_class = ListingForm
    template = 'listing/list.html'

    def populate_category_data(self, data, category_id):
        data['category'] = get_object_or_404(Category, id=category_id, active=True)

    def populate_listing_list_data(self, data, category):
        listing_list = Listing.objects.filter(category=category, active=True)
        data['listing_public_list'] = listing_list.filter(public=True)
        if is_admin(self.request.user):
            data['listing_private_list'] = listing_list.filter(public=False)

    def populate_form_data(self, data, *args, **kwargs):
        if is_admin(self.request.user):
            data['form'] = self.form_class(*args, **kwargs)

    def get(self, request, **kwargs):
        data = {}
        populate_nav_data(data)
        self.populate_category_data(data, kwargs['category_id'])
        self.populate_listing_list_data(data, data['category'])
        self.populate_form_data(data, initial={})
        return render(request, self.template, data)

    def post(self, request, **kwargs):
        if not is_admin(self.request.user):
            raise PermissionDenied
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
        if is_admin(self.request.user):
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
        if not is_admin(self.request.user):
            raise PermissionDenied
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
    data['admin_username'] = ADMIN
    data['category_list'] = Category.objects.filter(active=True)

def is_admin(user):
    return user.is_authenticated and user.username == ADMIN
