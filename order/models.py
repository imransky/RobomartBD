from django.db import models
from cart.models import Cart
from Basic_Api.models import User,Product,Cupon


class Delivary(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    is_served = models.BooleanField(default=False) #step :2
    is_payment_done = models.BooleanField(default=False) #step :1
    is_sell_done = models.BooleanField(default=False) #step :3
    is_cancel = models.BooleanField(default=False) #Step : Optional
    

    billing_option = models.CharField(max_length=100,default="CASH_ON_DELIVERY")
    payment_method = models.CharField(max_length=100,null=True,blank=True)
    payment_number = models.CharField(max_length=18,null=True,blank=True)
    payment_id = models.CharField(max_length=255,null=True,blank=True)

    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(blank=True,null=True)
    address = models.TextField(max_length=500,null=True,blank=True)
    phone = models.CharField(max_length=15,null=True,blank=True)

    cupon = models.ForeignKey(Cupon,on_delete=models.PROTECT,null=True,blank=True)


    delevary_location = models.ForeignKey(Delivary,on_delete=models.PROTECT,null=True,blank=True)
    price_after_add_copun = models.IntegerField(null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.user.email} => is_served: {self.is_served} => price : {self.total_price}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField(null=True,blank=True)
    quantity = models.IntegerField()
    def __str__(self) -> str:
        return f"{self.order.user.email} => Product : {self.product.name}"
        
        
class Invoice(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    status = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"ID:==>{self.id} OrderID==>{self.order.id}"  
