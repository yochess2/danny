from django.db import models

class Category(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=63, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Listing(models.Model):
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=127, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    display = models.ImageField(upload_to='images/', default='images/default.png')
    public = models.BooleanField(default=False)


    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

class Spec(models.Model):
    listing = models.OneToOneField('Listing', related_name='spec', null=True, on_delete=models.SET_NULL)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=63)
    state = models.CharField(max_length=63)
    zipcode = models.IntegerField()
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    building_size = models.IntegerField(null=True, blank=True)
    property_type = models.CharField(max_length=31, null=True, blank=True)
    description = models.TextField(max_length=4047, null=True, blank=True)
