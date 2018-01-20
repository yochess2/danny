from rest_framework import serializers

from listings.models import Listing, Category, Spec
from userprofile.models import Profile

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'url', 'active', 'title', 'created')


class ListingSerializer(serializers.HyperlinkedModelSerializer):
    spec = serializers.HyperlinkedRelatedField(view_name='spec-detail', read_only=True)

    class Meta:
        model = Listing
        fields = ('id', 'url', 'active', 'title', 'created', 'category', 'spec', 'display', 'public')


class SpecSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Spec
        fields = (
            'id', 'url', 'address', 'city', 'state', 'zipcode', 'bedrooms',
            'bathrooms', 'building_size', 'property_type', 'description', 'listing'
        )


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'url', 'active', 'biography', 'display')
