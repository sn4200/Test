
from django.db import models

class Warehouse(models.Model):
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=100)
	sku = models.CharField(max_length=50, unique=True)
	quantity = models.PositiveIntegerField(default=0)
	warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='items')

	def __str__(self):
		return f"{self.name} ({self.sku})"

class Order(models.Model):
	order_number = models.CharField(max_length=50, unique=True)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	order_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Order {self.order_number}"
