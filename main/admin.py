from django.contrib import admin

# Register your models here.
from main.models import Customer, Location
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name','slug',)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('date','address',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Location, LocationAdmin)