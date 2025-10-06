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
from viastore_app.views import dashboard, add_warehouse, add_item, add_order, goods_receipt, stock_correction, stock_info, item_bestand_api, order_list, goods_receipt_touch, login_view, logout_view, import_excel
from viastore_app.views_touch import touch_main, item_info_api
from viastore_app.views_touch import touch_main, item_info_api, google_item_info_api
from viastore_app.views_item import item_list, item_edit, item_delete


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
    path("artikel/", item_list, name="item_list"),
    path("artikel/<int:pk>/bearbeiten/", item_edit, name="item_edit"),
    path("artikel/<int:pk>/loeschen/", item_delete, name="item_delete"),
    path("lager-anlegen/", add_warehouse, name="add_warehouse"),
    path("artikel-anlegen/", add_item, name="add_item"),
    path("bestellung-anlegen/", add_order, name="add_order"),
    path("wareneingang/", goods_receipt, name="goods_receipt"),
    path("bestandskorrektur/", stock_correction, name="stock_correction"),
    path("bestandsauskunft/", stock_info, name="stock_info"),
    path("api/item-bestand/<int:item_id>/", item_bestand_api, name="item_bestand_api"),
    path("api/item-info/<str:sku>/", item_info_api, name="item_info_api"),
        path("api/google-item-info/<str:sku>/", google_item_info_api, name="google_item_info_api"),
    path("bestellungen/", order_list, name="order_list"),
    path("wareneingang-touch/", touch_main, name="goods_receipt_touch"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("touch/", touch_main, name="touch_main"),
    path("import-excel/", import_excel, name="import_excel"),
]
