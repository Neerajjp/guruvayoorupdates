from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from main import views as general_views


urlpatterns = [
    path('default-dashboard/', admin.site.urls),

    path('app/accounts/', include('registration.backends.default.urls')),
    path('app/', general_views.app, name='app'),
    path('app/dashboard/', general_views.dashboard, name='dashboard'),

    path('', include(('web.urls', 'web'), namespace='web')),
    path('users/', include('users.urls', namespace='users')),
    path('app/main/', include('main.urls', namespace='main')), 
    path('app/customers/', include(('customers.urls', 'customers'), namespace='customers')),
    path('app/orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('app/products/', include(('products.urls', 'products'), namespace='products')),
    path('app/general/', include(('general.urls', 'general'), namespace='general')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
