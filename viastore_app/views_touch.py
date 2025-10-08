import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class GoogleItemInfoAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, sku):
        bezeichnung = str(sku)
        try:
            url = f"https://www.google.com/search?q={sku}"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.ok:
                soup = BeautifulSoup(resp.text, "html.parser")
                autodoc_link = None
                for a in soup.find_all("a", href=True):
                    if "autodoc.de" in a["href"] and a.text.strip():
                        autodoc_link = a
                        break
                if autodoc_link:
                    bezeichnung = autodoc_link.text.strip()
        except Exception:
            pass
        return Response({"name": bezeichnung})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ItemInfoAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, sku):
        from .models import Item
        item = Item.objects.filter(sku=str(sku)).first()
        if item:
            data = {"name": item.name}
        else:
            data = {"error": "Artikel nicht gefunden"}
        return Response(data)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .forms import TouchGoodsReceiptForm
from .models import Item, Warehouse

class TouchMainAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        form = TouchGoodsReceiptForm(request.data)
        if form.is_valid():
            artikelnummer = form.cleaned_data["item_name"]
            quantity = form.cleaned_data["quantity"]
            item = Item.objects.filter(sku=str(artikelnummer)).first()
            if not item:
                bezeichnung = str(artikelnummer)
                try:
                    url_json = f"https://world.openfoodfacts.org/api/v0/product/{artikelnummer}.json"
                    resp = requests.get(url_json, timeout=5)
                    if resp.ok:
                        data = resp.json()
                        if 'product' in data and 'product_name' in data['product'] and data['product']['product_name']:
                            bezeichnung = data['product']['product_name']
                except Exception:
                    pass
                warehouse = Warehouse.objects.first()
                item = Item.objects.create(name=str(artikelnummer), sku=bezeichnung, quantity=0, warehouse=warehouse)
            item.quantity += quantity
            item.save()
            return Response({"message": f"Wareneingang für {item.name} ({item.sku}) erfolgreich gebucht!"})
        return Response({"error": "Ungültige Daten"}, status=400)
