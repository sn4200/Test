from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Warehouse, Item, Order
from .forms import WarehouseForm, ItemForm, OrderForm, GoodsReceiptForm, StockCorrectionForm

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
	return render(request, "goods_receipt_touch.html", {"form": form, "title": "Wareneingang Touch", "message": message})
def order_list(request):
	orders = Order.objects.select_related('item').all().order_by('-order_date')
	return render(request, "order_list.html", {"orders": orders, "title": "Bestellungen"})
from django.http import JsonResponse
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
def stock_info(request):
	items = Item.objects.select_related('warehouse').all()
	return render(request, "stock_info.html", {"items": items, "title": "Bestandsauskunft"})
from django.shortcuts import render, redirect
from .models import Warehouse, Item, Order
from .forms import WarehouseForm, ItemForm, OrderForm, GoodsReceiptForm, StockCorrectionForm
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
	return render(request, "form.html", {"form": form, "title": "Bestandskorrektur", "current_quantity": current_quantity, "selected_item": selected_item})

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

def add_warehouse(request):
	if request.method == "POST":
		form = WarehouseForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("dashboard")
	else:
		form = WarehouseForm()
	return render(request, "form.html", {"form": form, "title": "Lager anlegen"})

def add_item(request):
	if request.method == "POST":
		form = ItemForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("dashboard")
	else:
		form = ItemForm()
	return render(request, "form.html", {"form": form, "title": "Artikel anlegen"})

def add_order(request):
	if request.method == "POST":
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("dashboard")
	else:
		form = OrderForm()
	return render(request, "form.html", {"form": form, "title": "Bestellung anlegen"})

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
