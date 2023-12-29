from django.urls import path, re_path
from products import views


app_name = "products"

urlpatterns = [
    re_path(r'^sub-category-autocomplete/$',views.SubCategoryAutocomplete.as_view(),name='sub_category_autocomplete'),
    re_path(r'categories/$', views.categories, name="categories"),
    re_path(r'^category/delete(?P<pk>.*)/$',views.delete_category, name="delete_category"),

    re_path(r'^sub-categories$', views.sub_categories, name='sub_categories'),
    re_path(r'^sub-category/delete/(?P<pk>.*)/$',views.delete_subcategory, name='delete_subcategory'),

    re_path(r'^products/create/$', views.create_product, name="create_product"),
    re_path(r'products/$', views.products, name="products"),
    re_path(r'^product/view/(?P<pk>.*)/$', views.product, name="product"),
    re_path(r'^product/edit/(?P<pk>.*)/$',views.edit_product, name="edit_product"),
    re_path(r'^product/delete/(?P<pk>.*)/$',views.delete_product, name="delete_product"),

    re_path(r'^create-product-variant/(?P<pk>.*)/$', views.create_product_variant, name="create_product_variant"),
    re_path(r'^product-variant/view/(?P<pk>.*)/$', views.product_variant, name="product_variant"),
    re_path(r'^product-variant/edit/(?P<pk>.*)/$',views.edit_product_variant, name="edit_product_variant"),
    re_path(r'^product-variant/delete(?P<pk>.*)/$',views.delete_product_variant, name="delete_product_variant"),
]