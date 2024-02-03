from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from cart.models import CartItem,Cart

from Basic_Api.models import Cupon
class GetOrder(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format = None):
        obj = Order.objects.filter(user=request.user)  
        ser = OrderSerializer(obj,many = True)
        return Response(ser.data)

    def post(self,request,format = None):
        obj = Order(user=request.user)
        obj.save()
        data = request.data
        if "items" not in data:
            return Response({'error':'Unvalid Body Please provide product info ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "delevary" not in data:
            return Response({'error':'Unvalid Body Please provide delevary info ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "phone" not in data:
            return Response({'error':'Unvalid Body Please provide phone info ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "address" not in data:
            return Response({'error':'Unvalid Body Please provide phone info ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "cupon" not in data:
            return Response({'error':'Unvalid Body Please provide cupon info ..'},status=status.HTTP_406_NOT_ACCEPTABLE)



        if "payment_method" not in data:
            return Response({'error':'Unvalid Body Please provide payment Method ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "payment_id" not in data:
            return Response({'error':'Unvalid Body Please provide payment id ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "payment_number" not in data:
            return Response({'error':'Unvalid Body Please provide payment_number ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "billing_option" not in data:
            return Response({'error':'Unvalid Body Please provide Billing Options ..'},status=status.HTTP_406_NOT_ACCEPTABLE)

        price = 0
        try:
            delevary = Delivary.objects.get(code=data['delevary'])
        except(ObjectDoesNotExist):
            return Response({'error':'Unvalid Delevary details please add some delevary option.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if data['cupon'] != None:
            try:
                copun = Cupon.objects.get(cupun_code=data['cupon'])
            except(ObjectDoesNotExist):
                return Response({'error':'Unvalid Copun Please cheak ..'},status=status.HTTP_404_NOT_FOUND)
        else:
            copun = None
        price+=delevary.price
        for i in data['items']:
            try:
                product = Product.objects.get(id=i['product']['id'])
            except(ObjectDoesNotExist):
                return Response({'error':'Unvalid Product Details Please cheak ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if "id" not in i:
                pass
            else:
                try:
                    cartitem = CartItem.objects.get(id=i["id"])
                except(ObjectDoesNotExist):
                    return Response({'error':'Unvalid CartItem Details Please cheak ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
                try:
                    cart = Cart.objects.get(user = request.user)

                except(ObjectDoesNotExist):
                    return Response({'error':'Do You have a cart ? ..'},status=status.HTTP_406_NOT_ACCEPTABLE)
                
                if cart.price >= (cartitem.product.price*cartitem.quantity):
                    cart.price-= (cartitem.product.price*cartitem.quantity)
                    cart.save()
                
                else:
                    cart.price = 0
                    cart.save()
                cart.count-=1
                cart.save()
                cartitem.delete()
                
            item_price = product.price*i['quantity']
            price+=item_price
            order_item = OrderItem(order=obj,product=product,quantity=i['quantity'],price =item_price )
            order_item.save()
       

        if copun!=None and copun.active:
            
            price_condition = copun.price_condition
            discount = copun.discount_in_percentage

            if price>=price_condition:
                price-= discount
                obj.price_after_add_copun = discount
        
        else:
            obj.price_after_add_copun = 0

        if data['billing_option'] == "BALANCE":
            if request.user.balance >= price:
                obj.payment_method = "BALANCE"
                obj.is_payment_done = True
                user = User.objects.get(email=request.user.email)
                obj.billing_option = "BALANCE"
                user.balance-=price
                user.save()
            
            else:
                obj.delete()
                return Response({'error':f'You dont have {price} TK balance .'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        elif data['billing_option'] == "MANUAL":
            if data['payment_id'] == None:
                obj.delete()
                return Response({'error':'You want to manual Payment But You do not provide any payment id'},status=status.HTTP_406_NOT_ACCEPTABLE)
            if data['payment_method'] == None:
                obj.delete()
                return Response({'error':'You want to manual Payment But You do not provide any payment method'},status=status.HTTP_406_NOT_ACCEPTABLE)
            if data['payment_number'] == None:
                obj.delete()
                return Response({'error':'You want to manual Payment But You do not provide any payment number'},status=status.HTTP_406_NOT_ACCEPTABLE)        

            obj.billing_option = "MANUAL"
            obj.payment_id = data['payment_id']
            obj.payment_method = data['payment_method']
            obj.payment_number = data['payment_number']

        else:
            pass
                
        obj.total_price = price
        obj.address = data['address']
        obj.phone = data['phone']
        obj.delevary_location = delevary
        obj.cupon = copun
        obj.save()
        obj_ser = OrderSerializer(obj)
        if data['billing_option'] == "CASH_ON_DELIVERY":
            statuss = 'UNPAID'
        else:
            statuss = 'PAID'
        invoice = Invoice.objects.create(order = obj, status = statuss)

        return Response(obj_ser.data,status=status.HTTP_201_CREATED)
    
    """
    def delete(self,request,format = None):
        print("Hello world")
        data = request.data
        product = Product.objects.get(id=data['product'])
        obj = Cart.objects.get(user = request.user)
        obj.products.remove(product)
        obj.count = obj.products.all().count()
        obj.save()
        ser = CartSerializerList(obj)
        return Response(ser.data)
"""

class CheakCupon(APIView):

    def post(self,request,format = None):
        data = request.data

        if 'cupon' not in data:
            return Response({'error':'Which Copun You want to Cheak . mention in body'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if 'total_price' not in data:
            return Response({'error':'Please Provide Total Price'},status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            copun = Cupon.objects.get(cupun_code=data['cupon'])
        except(ObjectDoesNotExist):
            return Response({'error':'no active cupon found'},status=status.HTTP_404_NOT_FOUND)
        
        total_price = data['total_price']

        if copun.active and copun.price_condition <=total_price:
            return Response({'Success':'you get some discount','discount':copun.discount_in_percentage},status=status.HTTP_200_OK)
        else:
            return Response({'error':'no active copun found Condition Dont match'},status=status.HTTP_404_NOT_FOUND)
        