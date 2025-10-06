
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Warehouse, Item, Order
from .forms import WarehouseForm, ItemForm, OrderForm, GoodsReceiptForm, StockCorrectionForm, ExcelImportForm
import openpyxl

@login_required
def import_excel(request):
	message = None
	if request.method == "POST":
		form = ExcelImportForm(request.POST, request.FILES)
		if form.is_valid():
			file = form.cleaned_data["file"]
			wb = openpyxl.load_workbook(file)
			ws = wb.active
			imported = 0
			for row in ws.iter_rows(min_row=2, values_only=True):
				# Beispiel: Name, SKU, Menge, Lagername
				name, sku, quantity, warehouse_name = row
				warehouse, _ = Warehouse.objects.get_or_create(name=warehouse_name)
				item, created = Item.objects.get_or_create(sku=sku, defaults={"name": name, "quantity": quantity, "warehouse": warehouse})
				if not created:
					item.name = name
					item.quantity = quantity
					item.warehouse = warehouse
					item.save()
				imported += 1
			message = f"{imported} Artikel importiert/aktualisiert."
	else:
		form = ExcelImportForm()
	return render(request, "import_excel.html", {"form": form, "message": message, "title": "Excel-Import"})

def logout_view(request):
	logout(request)
	return redirect("login")

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
def goods_receipt_touch(request):
	from .forms import GoodsReceiptForm
	message = None
	if request.method == "POST":
		form = GoodsReceiptForm(request.POST)
		if form.is_valid():
			item = form.cleaned_data["item"]
			quantity = form.cleaned_data["quantity"]
			item.quantity += quantity
			item.save()
			message = f"Wareneingang für {item.name} ({item.sku}) erfolgreich gebucht!"
			form = GoodsReceiptForm()
	else:
		form = GoodsReceiptForm()
	context = {"form": form, "title": "Wareneingang Touch", "message": message}
	if request.GET.get("ajax") == "1":
		return render(request, "goods_receipt_touch.html", context)
	return render(request, "goods_receipt_touch.html", context)
@login_required
def order_list(request):
	orders = Order.objects.select_related('item').all().order_by('-order_date')
	return render(request, "order_list.html", {"orders": orders, "title": "Bestellungen"})
from django.http import JsonResponse
@login_required
def item_bestand_api(request, item_id):
	try:
		item = Item.objects.get(pk=item_id)
		data = {
			"name": item.name,
			"sku": item.sku,
			"quantity": item.quantity
		}
		return JsonResponse(data)
	except Item.DoesNotExist:
		return JsonResponse({"error": "Artikel nicht gefunden"}, status=404)
@login_required
def stock_info(request):
	items = Item.objects.select_related('warehouse').all()
	return render(request, "stock_info.html", {"items": items, "title": "Bestandsauskunft"})
from django.shortcuts import render, redirect
from .models import Warehouse, Item, Order
from .forms import WarehouseForm, ItemForm, OrderForm, GoodsReceiptForm, StockCorrectionForm
@login_required
def stock_correction(request):
	current_quantity = None
	selected_item = None
	if request.method == "POST":
		form = StockCorrectionForm(request.POST)
		if form.is_valid():
			item = form.cleaned_data["item"]
			new_quantity = form.cleaned_data["new_quantity"]
			item.quantity = new_quantity
			item.save()
			if request.GET.get("ajax") == "1":
				return render(request, "form.html", {"form": StockCorrectionForm(), "title": "Bestandskorrektur", "message": "Bestand erfolgreich korrigiert!", "ajax": True})
			return redirect("dashboard")
		if form.cleaned_data.get("item"):
			selected_item = form.cleaned_data["item"]
			current_quantity = selected_item.quantity
	else:
		form = StockCorrectionForm()
	# Wenn ein Item ausgewählt ist, zeige den aktuellen Bestand
	if request.method == "GET" and request.GET.get("item"):
		try:
			selected_item = Item.objects.get(pk=request.GET.get("item"))
			current_quantity = selected_item.quantity
		except Item.DoesNotExist:
			current_quantity = None
	context = {"form": form, "title": "Bestandskorrektur", "current_quantity": current_quantity, "selected_item": selected_item, "ajax": request.GET.get("ajax") == "1"}
	return render(request, "form.html", context)

@login_required
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
