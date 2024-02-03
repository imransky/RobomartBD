from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class GetCartProducts(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format = None):
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            cart = Cart(user=request.user,count=0,price=0)
            cart.save()
        # Need to Do Cart price validationnn...
        cart_ser = CartSerializerList(cart,context={'request':request})
        return Response(cart_ser.data,status=status.HTTP_200_OK)
    
    def post(self,request,format = None):
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            cart = Cart(user=request.user,count=0,price=0)
            cart.save()
        data = request.data
        if 'product' not in data:
            return Response({"error":"Give product id please."},status=status.HTTP_406_NOT_ACCEPTABLE)
        if 'quantity' not in data:
            return Response({"error":"Give quantity please."},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        
        product =Product.objects.get(id=data["product"])
        cart_item_data = CartItem.objects.filter(cart=cart,product=product)
        if cart_item_data.exists():
            cart_item = cart_item_data.first()
            cart_item.quantity += data["quantity"]
            cart_item.save()
            
            
            cart.price+=(product.price*data["quantity"])
            cart.save()
            ser = CartSerializerList(cart,context={'request':request})
            return Response(ser.data,status=status.HTTP_201_CREATED)
        cart.count+=1
        cart.price+=(product.price*data["quantity"])
        cart.save()
        cart_item = CartItem(product=product,quantity=data["quantity"],cart = cart)
        cart_item.save()
        ser = CartSerializerList(cart,context={'request':request})
        return Response(ser.data,status=status.HTTP_201_CREATED)
    
    def delete(self,request,format = None):
        data = request.data
        if "id" not in data:
            return Response({"error":"Give some Data"},status=status.HTTP_406_NOT_ACCEPTABLE)
        try:       
            obj = CartItem.objects.get(id = data['id'])
        except:
            return Response({"error":"Did you send valid Cart Item id ? "},status=status.HTTP_404_NOT_FOUND)
        if request.user == obj.cart.user:
            try:
                cart = Cart.objects.get(user=request.user)
            except:
                return Response({"error":"Something Went Wrong"},status=status.HTTP_404_NOT_FOUND)
            
            if cart.price >= (obj.product.price*obj.quantity):
                cart.price-= (obj.product.price*obj.quantity)
                cart.save()
                
            else:
                cart.price = 0
                cart.save()
            cart.count-=1
            cart.save()
            obj.delete()
            return Response({"success": "Successfully Deleted"},status=status.HTTP_200_OK)
        else:
            return Response({"error":"You are not Owner of this Cartitem"},status=status.HTTP_401_UNAUTHORIZED)



# Neeed To Add Increase BY one and Decrease By one Functionality

class ControlQuantity(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        if 'flag' not in data:
            return Response({'error':'You missed Flag!.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if 'id' not in data:
            return Response({'error':'You missed id!.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        flag = data['flag']
        id_ = data['id']

        if flag=='i':
            try:
                objj = CartItem.objects.get(id=id_)
            except(ObjectDoesNotExist):
                return Response({'error':'You Provide a Unvalid Cartitem id that does not exist '},status=status.HTTP_404_NOT_FOUND)
            
            if request.user == objj.cart.user:
                cart = Cart.objects.get(user = request.user)
                objj.quantity+=1
                cart.price+= objj.product.price
                
                objj.save()
                cart.save()
                return Response({'success':"Okay Bro.."},status=status.HTTP_201_CREATED)
            else:
                return Response({'error':"You are Not the owner of this Cart item :) "},status=status.HTTP_404_NOT_FOUND)
            
        elif flag=='d':
            try:
                objj = CartItem.objects.get(id=id_)
            except(ObjectDoesNotExist):
                return Response({'error':'You Provide a Unvalid Cartitem id that does not exist '},status=status.HTTP_404_NOT_FOUND)
            if request.user == objj.cart.user:
                if objj.quantity >= 1:
                    cart = Cart.objects.get(user = request.user)
                    objj.quantity-=1
                    cart.price -= objj.product.price
                    objj.save()
                    if objj.quantity<=0:
                        objj.delete()
                        cart.count-=1
                    
                    cart.save()
                    return Response({'success':"Okay Bro.."},status=status.HTTP_201_CREATED)
                else:
                    objj.quantity = 0
                    objj.delete()
                    cart.count-=1

            else:
                return Response({'error':"You are Not the owner of this Cart item :) "},status=status.HTTP_404_NOT_FOUND)
            
        else:
            return Response({'error':'What you want to do ?'},status=status.HTTP_400_BAD_REQUEST)

            
class AddToCartByArray(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):

        try:
            cart = Cart.objects.get(user=request.user)
        except:
            cart = Cart(user=request.user,count=0,price=0)
            cart.save()
        d = request.data
        print(bool(d))
        if not bool(d):
            return Response({"error":"request data is empty !"},status=status.HTTP_406_NOT_ACCEPTABLE)
        for data in d:
            if 'product' not in data:
                return Response({"error":"Give product id please."},status=status.HTTP_406_NOT_ACCEPTABLE)
            if 'quantity' not in data:
                return Response({"error":"Give quantity please."},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            
            product =Product.objects.get(id=data["product"])
            cart_item_data = CartItem.objects.filter(cart=cart,product=product)
            if cart_item_data.exists():
                cart_item = cart_item_data.first()
                cart_item.quantity += data["quantity"]
                cart_item.save()
                
                
                cart.price+=(product.price*data["quantity"])
                cart.save()
                continue
            cart.count+=1
            cart.price+=(product.price*data["quantity"])
            cart.save()
            cart_item = CartItem(product=product,quantity=data["quantity"],cart = cart)
            cart_item.save()
            # ser = CartSerializerList(cart,context={'request':request})
        return Response({"success":"product added successfully"},status=status.HTTP_201_CREATED)