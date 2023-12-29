from django.contrib import admin
from general.models import Location, Help, ShopDetails, ChargePerKilometer, Faq


# Register your models here.
admin.site.register(Location)
admin.site.register(Help)
admin.site.register(ChargePerKilometer)
admin.site.register(ShopDetails)
admin.site.register(Faq)