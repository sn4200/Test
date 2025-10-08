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
from viastore_app.api_views import (
    TokenLoginView, DashboardAPIView, WarehouseListCreateAPIView,
    ItemListCreateAPIView, ItemDetailAPIView, ItemBestandAPIView,
    OrderListCreateAPIView, GoodsReceiptAPIView, StockCorrectionAPIView,
    StockInfoAPIView, ExcelImportAPIView, ItemInfoAPIView,
    GoogleItemInfoAPIView, TouchGoodsReceiptAPIView
)


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Authentication
    path("api/token-login/", TokenLoginView.as_view(), name="token_login"),
    
    # Dashboard
    path("api/dashboard/", DashboardAPIView.as_view(), name="dashboard"),
    
    # Warehouses
    path("api/lager/", WarehouseListCreateAPIView.as_view(), name="warehouse_list_create"),
    
    # Items
    path("api/artikel/", ItemListCreateAPIView.as_view(), name="item_list_create"),
    path("api/artikel/<int:pk>/", ItemDetailAPIView.as_view(), name="item_detail"),
    path("api/item-bestand/<int:item_id>/", ItemBestandAPIView.as_view(), name="item_bestand_api"),
    path("api/item-info/<str:sku>/", ItemInfoAPIView.as_view(), name="item_info_api"),
    
    # Orders
    path("api/bestellungen/", OrderListCreateAPIView.as_view(), name="order_list_create"),
    
    # Goods Receipt
    path("api/wareneingang/", GoodsReceiptAPIView.as_view(), name="goods_receipt"),
    path("api/wareneingang-touch/", TouchGoodsReceiptAPIView.as_view(), name="goods_receipt_touch"),
    
    # Stock Management
    path("api/bestandskorrektur/", StockCorrectionAPIView.as_view(), name="stock_correction"),
    path("api/bestandsauskunft/", StockInfoAPIView.as_view(), name="stock_info"),
    
    # Import
    path("api/import-excel/", ExcelImportAPIView.as_view(), name="import_excel"),
    
    # External data
    path("api/google-item-info/<str:sku>/", GoogleItemInfoAPIView.as_view(), name="google_item_info_api"),
]
