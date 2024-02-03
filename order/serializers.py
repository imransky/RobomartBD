from rest_framework import serializers
from django.db.models import QuerySet
from Basic_Api.models import User,Product
from rest_framework.fields import empty
from .models import Order,OrderItem,Invoice
from Basic_Api.serializers import ProductSerializerList,UserSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerList()
    class Meta:
        model = OrderItem
        fields = "__all__"
        
        
class InvoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Invoice
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    invoiceId = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ('id','email','total_price','order_date','is_served','is_payment_done','is_sell_done','address','phone','items','invoiceId')

    def get_email(self,instance):

        return instance.user.email
    
    def get_items(self,instance):

        objj = OrderItem.objects.filter(order = instance)
        ser = OrderItemSerializer(objj, many = True)
        return ser.data

    def get_invoiceId(self,instance):
        
        try:
            invoice = Invoice.objects.filter(order=instance).first()
            
            if invoice is not None:
                return invoice.id
                
            else:
                return None
        except:
            return None




class OrderDetailsSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    shiping = serializers.SerializerMethodField()
    invoiceId = serializers.SerializerMethodField()
    user = UserSerializer()
    
    class Meta:
        model = Order
        fields = '__all__'

    def get_items(self,instance):
        objj = OrderItem.objects.filter(order = instance)
        print(objj)
        ser = OrderItemSerializer(objj,many = True,context=self._context)
        return ser.data
    
    def get_shiping(self,instance):
        return instance.delevary_location.price
    
    def get_invoiceId(self,instance):
        
        invoice = Invoice.objects.filter(order = instance).first()
        print(invoice.id)
            
        if invoice is not None:
            ser = InvoiceSerializer(invoice)
            return ser.data
            
        else:
            return None


 