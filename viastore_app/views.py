
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.permissions import IsAuthenticated
from .models import Warehouse, Item, Order
from .forms import WarehouseForm, ItemForm, OrderForm, GoodsReceiptForm, StockCorrectionForm, ExcelImportForm
import openpyxl


class ImportExcelAPIJWT(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		form = ExcelImportForm(request.data, request.FILES)
		if form.is_valid():
			file = form.cleaned_data["file"]
			wb = openpyxl.load_workbook(file)
			ws = wb.active
			imported = 0
			for row in ws.iter_rows(min_row=2, values_only=True):
				name, sku, quantity, warehouse_name = row
				warehouse, _ = Warehouse.objects.get_or_create(name=warehouse_name)
				item, created = Item.objects.get_or_create(sku=sku, defaults={"name": name, "quantity": quantity, "warehouse": warehouse})
				if not created:
					item.name = name
					item.quantity = quantity
					item.warehouse = warehouse
					item.save()
				imported += 1
			return Response({"message": f"{imported} Artikel importiert/aktualisiert."})
		return Response({"error": "Ungültige Daten"}, status=400)

def logout_view(request):
	logout(request)
	return redirect("login")

# JWT Login API
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class LoginJWTView(APIView):
	authentication_classes = []
	permission_classes = []

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			refresh = RefreshToken.for_user(user)
			return Response({
				'refresh': str(refresh),
				'access': str(refresh.access_token),
			})
		return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect("dashboard")
	else:
		form = AuthenticationForm()
	return render(request, "login.html", {"form": form, "title": "Login"})
@login_required
def order_list(request):
	orders = Order.objects.select_related('item').all().order_by('-order_date')
	return render(request, "order_list.html", {"orders": orders, "title": "Bestellungen"})
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ItemBestandAPIJWT(APIView):
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
			return Response({"error": "Artikel nicht gefunden"}, status=404)

def dashboard(request):
	warehouses = Warehouse.objects.count()
	items = Item.objects.count()
	orders = Order.objects.count()
	context = {
		"warehouse_count": warehouses,
		"item_count": items,
		"order_count": orders,
	}
	return render(request, "dashboard.html", context)

@login_required
def add_warehouse(request):
	if request.method == "POST":
		form = WarehouseForm(request.POST)
		if form.is_valid():
			form.save()
			if request.GET.get("ajax") == "1":
				return render(request, "form.html", {"form": WarehouseForm(), "title": "Lager anlegen", "message": "Lager erfolgreich angelegt!", "ajax": True})
			return redirect("dashboard")
	else:
		form = WarehouseForm()
	context = {"form": form, "title": "Lager anlegen", "ajax": request.GET.get("ajax") == "1"}
	return render(request, "form.html", context)

@login_required
def add_item(request):
	if request.method == "POST":
		form = ItemForm(request.POST)
		if form.is_valid():
			form.save()
			if request.GET.get("ajax") == "1":
				return render(request, "form.html", {"form": ItemForm(), "title": "Artikel anlegen", "message": "Artikel erfolgreich angelegt!", "ajax": True})
			return redirect("dashboard")
	else:
		form = ItemForm()
	context = {"form": form, "title": "Artikel anlegen", "ajax": request.GET.get("ajax") == "1"}
	return render(request, "form.html", context)

@login_required
def add_order(request):
	if request.method == "POST":
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			if request.GET.get("ajax") == "1":
				return render(request, "form.html", {"form": OrderForm(), "title": "Bestellung anlegen", "message": "Bestellung erfolgreich angelegt!", "ajax": True})
			return redirect("dashboard")
	else:
		form = OrderForm()
	context = {"form": form, "title": "Bestellung anlegen", "ajax": request.GET.get("ajax") == "1"}
	return render(request, "form.html", context)

@login_required
def goods_receipt(request):
	if request.method == "POST":
		form = GoodsReceiptForm(request.POST)
		if form.is_valid():
			item = form.cleaned_data["item"]
			quantity = form.cleaned_data["quantity"]
			item.quantity += quantity
			item.save()
			return redirect("dashboard")
	else:
		form = GoodsReceiptForm()
	return render(request, "form.html", {"form": form, "title": "Wareneingang buchen"})
