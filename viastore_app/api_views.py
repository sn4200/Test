from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .models import Warehouse, Item, Order
from .serializers import (
    WarehouseSerializer, ItemSerializer, ItemDetailSerializer,
    OrderSerializer, GoodsReceiptSerializer, TouchGoodsReceiptSerializer,
    StockCorrectionSerializer
)
import openpyxl
import requests
from bs4 import BeautifulSoup


class TokenLoginView(TokenObtainPairView):
    """JWT Token Login endpoint"""
    permission_classes = [AllowAny]


class DashboardAPIView(APIView):
    """Dashboard statistics API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        warehouse_count = Warehouse.objects.count()
        item_count = Item.objects.count()
        order_count = Order.objects.count()
        
        return Response({
            'warehouse_count': warehouse_count,
            'item_count': item_count,
            'order_count': order_count
        })


class WarehouseListCreateAPIView(APIView):
    """List all warehouses or create a new warehouse"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemListCreateAPIView(APIView):
    """List all items or create a new item"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        items = Item.objects.all().order_by('name')
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailAPIView(APIView):
    """Retrieve, update or delete an item"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemDetailSerializer(item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemBestandAPIView(APIView):
    """Get item stock information"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            data = {
                "name": item.name,
                "sku": item.sku,
                "quantity": item.quantity
            }
            return Response(data)
        except Item.DoesNotExist:
            return Response({"error": "Artikel nicht gefunden"}, status=status.HTTP_404_NOT_FOUND)


class OrderListCreateAPIView(APIView):
    """List all orders or create a new order"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        orders = Order.objects.select_related('item').all().order_by('-order_date')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoodsReceiptAPIView(APIView):
    """Create goods receipt"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = GoodsReceiptSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.validated_data['item']
            quantity = serializer.validated_data['quantity']
            item.quantity += quantity
            item.save()
            return Response({
                'message': f'Wareneingang für {item.name} ({item.sku}) erfolgreich gebucht!',
                'item': ItemSerializer(item).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockCorrectionAPIView(APIView):
    """Correct item stock"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = StockCorrectionSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.validated_data['item']
            new_quantity = serializer.validated_data['new_quantity']
            old_quantity = item.quantity
            item.quantity = new_quantity
            item.save()
            return Response({
                'message': 'Bestand erfolgreich korrigiert!',
                'item': ItemSerializer(item).data,
                'old_quantity': old_quantity,
                'new_quantity': new_quantity
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockInfoAPIView(APIView):
    """Get stock information for all items"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        items = Item.objects.select_related('warehouse').all()
        serializer = ItemDetailSerializer(items, many=True)
        return Response(serializer.data)


class ExcelImportAPIView(APIView):
    """Import items from Excel file"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        
        try:
            wb = openpyxl.load_workbook(file)
            ws = wb.active
            imported = 0
            
            for row in ws.iter_rows(min_row=2, values_only=True):
                # Example: Name, SKU, Quantity, Warehouse name
                if not row or len(row) < 4:
                    continue
                
                name, sku, quantity, warehouse_name = row
                warehouse, _ = Warehouse.objects.get_or_create(name=warehouse_name)
                item, created = Item.objects.get_or_create(
                    sku=sku, 
                    defaults={"name": name, "quantity": quantity, "warehouse": warehouse}
                )
                
                if not created:
                    item.name = name
                    item.quantity = quantity
                    item.warehouse = warehouse
                    item.save()
                
                imported += 1
            
            return Response({
                'message': f'{imported} Artikel importiert/aktualisiert.',
                'imported_count': imported
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': f'Fehler beim Import: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class ItemInfoAPIView(APIView):
    """Get item information by SKU"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, sku):
        item = Item.objects.filter(sku=str(sku)).first()
        if item:
            data = {"name": item.name, "sku": item.sku, "quantity": item.quantity}
        else:
            data = {"error": "Artikel nicht gefunden"}
        return Response(data)


class GoogleItemInfoAPIView(APIView):
    """Get item information from Google search"""
    permission_classes = [AllowAny]
    
    def get(self, request, sku):
        bezeichnung = str(sku)
        try:
            url = f"https://www.google.com/search?q={sku}"
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.ok:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Search for first link to autodoc.de
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


class TouchGoodsReceiptAPIView(APIView):
    """Touch interface for goods receipt"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TouchGoodsReceiptSerializer(data=request.data)
        if serializer.is_valid():
            artikelnummer = serializer.validated_data['item_name']
            quantity = serializer.validated_data['quantity']
            
            # Check if item exists
            item = Item.objects.filter(sku=str(artikelnummer)).first()
            
            if not item:
                # Fetch product name from web API
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
                
                # Create new item
                warehouse = Warehouse.objects.first()
                if not warehouse:
                    return Response({
                        'error': 'Kein Lager vorhanden. Bitte legen Sie zuerst ein Lager an.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                item = Item.objects.create(
                    name=str(artikelnummer),
                    sku=bezeichnung,
                    quantity=0,
                    warehouse=warehouse
                )
            
            # Update quantity
            item.quantity += quantity
            item.save()
            
            return Response({
                'message': f'Wareneingang für {item.name} ({item.sku}) erfolgreich gebucht!',
                'item': ItemSerializer(item).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
