from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .forms import ItemForm
from django.shortcuts import get_object_or_404

class ItemListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        items = Item.objects.all().order_by('name')
        data = [{
            "id": i.id,
            "name": i.name,
            "sku": i.sku,
            "quantity": i.quantity
        } for i in items]
        return Response({"items": data})

class ItemEditAPI(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(request.data, instance=item)
        if form.is_valid():
            form.save()
            return Response({"message": "Artikel erfolgreich bearbeitet!"})
        return Response({"error": "Ungültige Daten"}, status=400)

class ItemDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response({"message": "Artikel gelöscht!"})
