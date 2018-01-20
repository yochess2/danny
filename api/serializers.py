from rest_framework import serializers

from listings.models import Listing, Category, Spec
from userprofile.models import Profile

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    def validate_title(self, value):
        if Category.objects.filter(active=True, title=value).count() > 0:
            raise serializers.ValidationError("Title already exists!")
        return value

    class Meta:
        model = Category
        fields = ('id', 'url', 'title', 'created')


class ListingSerializer(serializers.HyperlinkedModelSerializer):
    spec = serializers.HyperlinkedRelatedField(view_name='spec-detail', read_only=True)

    def validate_title(self, value):
        if Listing.objects.filter(active=True, title=value).count() > 0:
            raise serializers.ValidationError("Title already exists!")
        return value

    class Meta:
        model = Listing
        fields = ('id', 'url', 'title', 'created', 'category', 'spec', 'display', 'public')


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
        fields = ('id', 'url', 'biography', 'display')
