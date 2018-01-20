from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from listings.models import Category, Listing, Spec
from userprofile.models import Profile
from .serializers import CategorySerializer, ListingSerializer, SpecSerializer, ProfileSerializer
from .permissions import IsAdminOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'listings': reverse('listing-list', request=request, format=format),
        'specs': reverse('spec-list', request=request, format=format),
        'categories': reverse('category-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format)
    })


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


class ListingList(generics.ListCreateAPIView):
    queryset = Listing.objects.filter(active=True)
    serializer_class = ListingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class ListingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.filter(active=True)
    serializer_class = ListingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


class SpecList(generics.ListCreateAPIView):
    queryset = Spec.objects.filter(listing__active=True)
    serializer_class = SpecSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class SpecDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Spec.objects.filter(listing__active=True)
    serializer_class = SpecSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()
