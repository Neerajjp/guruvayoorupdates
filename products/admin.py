from django.contrib import admin
from products.models import Product, ProductVariant, Category, SubCategory


admin.site.register(Product)
admin.site.register(ProductVariant)
# admin.site.register(ProductVariantImages)
admin.site.register(Category)
admin.site.register(SubCategory)