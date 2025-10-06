"""
URL configuration for viastore_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from viastore_app.views import dashboard, add_warehouse, add_item, add_order, goods_receipt, stock_correction, stock_info, item_bestand_api, order_list, goods_receipt_touch, login_view, logout_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("lager-anlegen/", add_warehouse, name="add_warehouse"),
    path("artikel-anlegen/", add_item, name="add_item"),
    path("bestellung-anlegen/", add_order, name="add_order"),
    path("wareneingang/", goods_receipt, name="goods_receipt"),
    path("bestandskorrektur/", stock_correction, name="stock_correction"),
    path("bestandsauskunft/", stock_info, name="stock_info"),
    path("api/item-bestand/<int:item_id>/", item_bestand_api, name="item_bestand_api"),
    path("bestellungen/", order_list, name="order_list"),
    path("wareneingang-touch/", goods_receipt_touch, name="goods_receipt_touch"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
