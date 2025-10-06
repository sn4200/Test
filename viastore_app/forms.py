from django import forms
from .models import Warehouse, Item, Order

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'location']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'sku', 'quantity', 'warehouse']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_number', 'item', 'quantity']


class GoodsReceiptForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    quantity = forms.IntegerField(min_value=1)

class StockCorrectionForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    new_quantity = forms.IntegerField(min_value=0, label="Neuer Bestand")
