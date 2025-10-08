from rest_framework import serializers
from .models import Warehouse, Item, Order


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']


class ItemSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'sku', 'quantity', 'warehouse', 'warehouse_name']


class ItemDetailSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    warehouse_location = serializers.CharField(source='warehouse.location', read_only=True)
    
    class Meta:
        model = Item
        fields = ['id', 'name', 'sku', 'quantity', 'warehouse', 'warehouse_name', 'warehouse_location']


class OrderSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_sku = serializers.CharField(source='item.sku', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'item', 'item_name', 'item_sku', 'quantity', 'order_date']


class GoodsReceiptSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class TouchGoodsReceiptSerializer(serializers.Serializer):
    item_name = serializers.IntegerField(label="Artikelnummer")
    quantity = serializers.IntegerField(min_value=1, label="Menge")


class StockCorrectionSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    new_quantity = serializers.IntegerField(min_value=0)
