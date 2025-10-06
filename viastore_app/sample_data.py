from viastore_app.models import Warehouse, Item, Order

# Beispiel-Lager
w1 = Warehouse.objects.create(name="Lager Nord", location="Hamburg")
w2 = Warehouse.objects.create(name="Lager Süd", location="München")

# Beispiel-Artikel
i1 = Item.objects.create(name="Gabelstapler", sku="STAPLER001", quantity=5, warehouse=w1)
i2 = Item.objects.create(name="Regal", sku="REGAL002", quantity=20, warehouse=w2)
i3 = Item.objects.create(name="Palette", sku="PAL003", quantity=100, warehouse=w1)

# Beispiel-Bestellungen
Order.objects.create(order_number="ORD1001", item=i1, quantity=2)
Order.objects.create(order_number="ORD1002", item=i2, quantity=5)
Order.objects.create(order_number="ORD1003", item=i3, quantity=10)
