from django.db import models
from Basic_Api.models import User,Product


class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True,null=True)
    count = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.user.email
    


    
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart,on_delete=models.PROTECT)


    def __str__(self) -> str:
        return self.cart.user.email
    
    