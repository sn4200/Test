
from django import forms
from .models import Warehouse, Item, Order

class ExcelImportForm(forms.Form):
    file = forms.FileField(label="Excel-Datei (.xlsx)")

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



# Standard-Formular für klassische Ansicht
class GoodsReceiptForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    quantity = forms.IntegerField(min_value=1)

# Touch-Formular mit Textfeld für Artikel
class TouchGoodsReceiptForm(forms.Form):
    item_name = forms.IntegerField(label="Artikelnummer")
    quantity = forms.IntegerField(min_value=1, label="Menge")

class StockCorrectionForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all())
    new_quantity = forms.IntegerField(min_value=0, label="Neuer Bestand")
