from django.db import models

from Basic_Api.models import Product,User


class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    ratting = models.FloatField()
    review = models.TextField(max_length=500)

    def __str__(self) -> str:
        return f"{self.user.email} => Product : {self.product.name} => Ratting : {self.ratting}"
