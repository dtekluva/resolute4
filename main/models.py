from django.db import models
from django.template.defaultfilters import slugify
from datetime import date

# Create your models here.
class Customer(models.Model):
    name            = models.CharField(max_length=40,unique=False)
    surname         = models.CharField(max_length=40,unique=False)
    phone            = models.IntegerField(unique=False, default = "0803312244")
    userid          = models.IntegerField(default=0)
    lng             = models.FloatField(max_length=100,blank=True, default=0)
    lat             = models.FloatField(max_length=100,blank=True, default=0)
    slug            = models.SlugField(blank=True,unique=True)
    address         = models.TextField(default=0)
    panicked        = models.DateField(auto_now_add=True, blank=True)
    is_panicking    = models.BooleanField(default = False)
    date            = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):              # __unicode__ on Python 2
        return self.slug

    class Meta:
        ordering = ('slug',)

class Location(models.Model):
    customer        = models.ForeignKey('Customer', on_delete=models.CASCADE)
    lng             = models.FloatField(max_length=100,blank=True, default=0)
    lat             = models.FloatField(max_length=100,blank=True, default=0)
    speed           = models.FloatField(max_length=100,blank=True, default=0)
    accuracy        = models.FloatField(max_length=100,blank=True, default=0)
    address         = models.TextField(default=0)
    date            = models.DateTimeField(auto_now_add=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.customer.name

    class Meta:
        ordering = ('date',)