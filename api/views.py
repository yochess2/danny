from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from listings.models import Category, Listing, Spec
from userprofile.models import Profile
from api.serializers import CategorySerializer, ListingSerializer, SpecSerializer, ProfileSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'listings': reverse('listing-list', request=request, format=format),
        'specs': reverse('spec-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format)
    })


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListingList(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class SpecList(generics.ListCreateAPIView):
    queryset = Spec.objects.all()
    serializer_class = SpecSerializer


class SpecDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Spec.objects.all()
    serializer_class = SpecSerializer


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
