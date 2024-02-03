from django.db import models
from order.models import Order
class Sell(models.Model):

    order = models.ForeignKey(Order,on_delete=models.PROTECT)

    total_price = models.IntegerField()
    total_profit = models.IntegerField()

    date = models.DateField(auto_now_add=True)


class Contact(models.Model):
    
    name = models.CharField(max_length = 500)
    email = models.CharField(max_length = 100)
    msg = models.CharField(max_length = 1000)
    
    def __str__(self):
        return f"name: {self.name} Email: {self.email}"
