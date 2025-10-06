from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm

@login_required
def item_list(request):
    items = Item.objects.all().order_by('name')
    return render(request, "item_list.html", {"items": items, "title": "Artikelübersicht"})

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item_list")
    else:
        form = ItemForm(instance=item)
    return render(request, "form.html", {"form": form, "title": f"Artikel bearbeiten: {item.name}"})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        return redirect("item_list")
    return render(request, "item_confirm_delete.html", {"item": item, "title": f"Artikel löschen: {item.name}"})
