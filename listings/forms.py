from django import forms

from .models import Listing, Spec, Category

class CategoryForm(forms.ModelForm):
    def clean_title(self):
        data = self.cleaned_data['title']
        if Category.objects.filter(active=True, title=data).count() > 0:
            raise forms.ValidationError("Title already exists!")
        return data

    class Meta:
        model = Category
        fields = ['title']


class ListingForm(forms.ModelForm):
    def clean_title(self):
        data = self.cleaned_data['title']
        if Listing.objects.filter(active=True, title=data).count() > 0:
            raise forms.ValidationError("Title already exists!")
        return data

    class Meta:
        model = Listing
        fields = ['category', 'title', 'display', 'public']


class SpecForm(forms.ModelForm):
    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        if data == None:
            return data
        if data > 99999 or data < 0:
            raise forms.ValidationError("Zipcode must be 5 digits or less!")
        return data

    def clean_bedrooms(self):
        data = self.cleaned_data['bedrooms']
        if data == None:
            return data
        if data > 999 or data < 0:
            raise forms.ValidationError("Bedrooms must be between 0 and 999!")
        return data

    def clean_bathrooms(self):
        data = self.cleaned_data['bathrooms']
        if data == None:
            return data
        if data > 999 or data < 0:
            raise forms.ValidationError("Bathrooms must be between 0 and 999!")
        return data

    def clean_building_size(self):
        data = self.cleaned_data['building_size']
        if data == None:
            return data
        if data > 999999 or data < 0:
            raise forms.ValidationError("Building size must be between 0 and 999,999!")
        return data

    class Meta:
        model = Spec
        fields = [
            'address', 'city', 'state', 'zipcode', 'bedrooms', 'bathrooms',
            'building_size', 'property_type', 'description'
        ]
