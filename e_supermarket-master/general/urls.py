from django.urls import path, re_path
from general import views


app_name = "general"

urlpatterns = [ 
    re_path(r'^settings/$', views.shop_settings,name="shop_settings"),
    re_path(r'^tax-slabs/$', views.tax_slabs,name="tax_slabs"),

    re_path(r'^banner-images/$', views.banner_images,name="banner_images"),
    re_path(r'^banner_image/delete(?P<pk>.*)/$',views.delete_banner_image, name="delete_banner_image"),

    re_path(r'^pages/$', views.pages,name="pages"),
]