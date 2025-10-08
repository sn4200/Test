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
from viastore_app.views import ImportExcelAPIJWT, AddWarehouseAPIJWT, AddItemAPIJWT, AddOrderAPIJWT, GoodsReceiptAPIJWT, StockCorrectionAPIJWT, StockInfoAPIJWT, OrderListAPIJWT, GoodsReceiptTouchAPIJWT, ItemBestandAPIJWT, LoginJWTView
from viastore_app.views import LoginJWTView
from viastore_app.views_touch import touch_main, item_info_api
from viastore_app.views_touch import touch_main, item_info_api, google_item_info_api
from viastore_app.views_item import ItemListAPI, ItemEditAPI, ItemDeleteAPI


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/import-excel/", ImportExcelAPIJWT.as_view(), name="import_excel_api"),
    path("api/lager-anlegen/", AddWarehouseAPIJWT.as_view(), name="add_warehouse_api"),
    path("api/artikel-anlegen/", AddItemAPIJWT.as_view(), name="add_item_api"),
    path("api/artikel/", ItemListAPI.as_view(), name="item_list_api"),
    path("api/artikel/<int:pk>/bearbeiten/", ItemEditAPI.as_view(), name="item_edit_api"),
    path("api/artikel/<int:pk>/loeschen/", ItemDeleteAPI.as_view(), name="item_delete_api"),
    path("api/bestellung-anlegen/", AddOrderAPIJWT.as_view(), name="add_order_api"),
    path("api/wareneingang/", GoodsReceiptAPIJWT.as_view(), name="goods_receipt_api"),
    path("api/bestandskorrektur/", StockCorrectionAPIJWT.as_view(), name="stock_correction_api"),
    path("api/bestandsauskunft/", StockInfoAPIJWT.as_view(), name="stock_info_api"),
    path("api/bestellungen/", OrderListAPIJWT.as_view(), name="order_list_api"),
    path("api/wareneingang-touch/", GoodsReceiptTouchAPIJWT.as_view(), name="goods_receipt_touch_api"),
    path("api/item-bestand/<int:item_id>/", ItemBestandAPIJWT.as_view(), name="item_bestand_api"),
    path("api/token-login/", LoginJWTView.as_view(), name="token_login"),
]
