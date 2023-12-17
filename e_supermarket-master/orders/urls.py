from django.urls import path, re_path
from orders import views


app_name = "orders"

urlpatterns = [ 
    re_path(r'orders/$', views.orders, name="orders"),
    re_path(r'^order/(?P<pk>.*)/$', views.order, name="order"),
    re_path(r'^update-order-status/(?P<pk>.*)/$', views.update_order_status, name="update_order_status"),
]