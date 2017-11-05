"""logist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from logistapp import views as logistapp_views
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', logistapp_views.index, name='index'),
    url(r'^search/$', logistapp_views.search_item, name='search'),
    url(r'^post_office/$', logistapp_views.post_office, name='post_office'),
    url(r'^confirm_delivery/$', logistapp_views.confirm_delivery, name='confirm_delivery'),
    url(r'^registration_post_item/$', logistapp_views.registration_post_item, name='registration_post_item'),
    url(r'^arr_depa/$', logistapp_views.arr_depa, name='arr_depa'),
    url(r'^set_arr_dep/$', logistapp_views.set_arr_dep, name='set_arr_dep'),
    # url(r'^api/add_new_elevation/', logistapp_views.add_elevation, name='add_elevation'),
    # url(r'^api/add_new_item/', logistapp_views.new_item, name='new_item'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
