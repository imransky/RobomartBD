from rest_framework import serializers
from django.db.models import QuerySet
from Basic_Api.models import User,Product
from rest_framework.fields import empty
from .models import Cart,CartItem
from Basic_Api.serializers import ProductSerializer
from django.core.exceptions import ObjectDoesNotExist



        
class CartItemSerializers(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartItem
        fields = "__all__"



class CartSerializerList(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ("count","price","items",)

    def get_items(self,instance):
        cart_items = CartItem.objects.filter(cart=instance)
        # Cart Validation For Price Down Or Up
        
        ser_data = CartItemSerializers(cart_items,many=True)
        return ser_data.data


