from django.contrib import admin
from .models import Warehouse, Item, Order

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
	list_display = ("name", "location")

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ("name", "sku", "quantity", "warehouse")
	search_fields = ("name", "sku")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("order_number", "item", "quantity", "order_date")
	search_fields = ("order_number",)
