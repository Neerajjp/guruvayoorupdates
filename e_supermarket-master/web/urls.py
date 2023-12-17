from django.urls import path, re_path
from web import views


app_name = "web"

urlpatterns = [ 
    re_path(r'^$', views.index,name="index"),
    re_path(r'^contact/$', views.contact,name="contact"),
    re_path(r'^about/$', views.about,name="about"),

    re_path(r'^register/$', views.register,name="register"),
    re_path(r'^otp-send/$', views.otp_send, name="otp_send"),
    re_path(r'^login/$', views.customer_login,name="login"),
    re_path(r'^verify-otp/$', views.verify_otp,name="verify_otp"),
    re_path(r'^logout/$', views.customer_logout, name='logout'),

    re_path(r'^store/$', views.store,name="store"),
    re_path(r'^items/(?P<pk>.*)/$', views.items,name="items"),
    re_path(r'^item-details/(?P<pk>.*)/$', views.item_details,name="item_details"),

    re_path(r'^cart/$', views.cart,name="cart"),
    re_path(r'^add-to-cart/(?P<pk>.*)/$', views.add_to_cart,name="add_to_cart"),
    re_path(r'^cart-update/(?P<pk>.*)/$', views.cart_quantity_update,name="cart_update"),
    re_path(r'^remove-from-cart(?P<pk>.*)/$', views.remove_from_cart,name="remove_from_cart"),
    re_path(r'^clear-cart/$', views.clear_cart,name="clear_cart"),

    re_path(r'^checkout/$', views.checkout,name="checkout"),
    re_path(r'^place-order/$', views.place_order,name="place_order"),
    re_path(r'^orders/$', views.orders,name="orders"),
    re_path(r'^order-details/(?P<pk>.*)/$', views.order_details,name="order_details"),
]