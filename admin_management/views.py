from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from order.models import Order,OrderItem,Invoice
from order.serializers import OrderSerializer,OrderDetailsSerializer
from rest_framework import permissions
from .models import Sell, Contact
from datetime import timezone
from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
class IsOrderManager(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.groups.filter(name="OrderManager").exists():

            return True
        
        
        else:
            return False
        

class IsOrderOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        pk = view.kwargs.get('pk')
        try:
            order = Order.objects.get(id=pk)
        except:
            return False
        if request.user.email == order.user.email:
            return True
        
        
        else:
            return False
        
class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        return request.user.is_superuser
    

class OrderDetails(APIView):
    permission_classes = [IsOrderManager | IsOrderOwner]
    def get(self,request,pk):
        try:
            objj = Order.objects.get(id=pk)
        except(ObjectDoesNotExist):
            return Response({"error":"Object Not Found"},status=status.HTTP_404_NOT_FOUND)
        
        ser = OrderDetailsSerializer(objj,context={'request':request})

        return Response(ser.data,status=status.HTTP_200_OK)
        
        
class AllSuccessOrder(APIView):
    permission_classes = [IsOrderManager]
    def get(self,request):

        objj = Order.objects.filter(is_cancel = False,is_served = True,is_sell_done = True)
        
        ser = OrderDetailsSerializer(objj,context={'request':request},many=True)

        return Response(ser.data,status=status.HTTP_200_OK)

class AllCancelOrder(APIView):
    permission_classes = [IsOrderManager]
    def get(self,request):

        objj = Order.objects.filter(is_cancel = True)

        
        ser = OrderDetailsSerializer(objj,context={'request':request},many=True)

        return Response(ser.data,status=status.HTTP_200_OK)
        

class PendingOrderManagement(APIView):
    permission_classes = [IsOrderManager]
    def get(self,request):

        objj = Order.objects.filter(is_payment_done = False, is_cancel = False)
        ser = OrderSerializer(objj,many = True)
        return Response(ser.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        data = request.data 
        if "orderid" not in data:
            return Response({"error":"Provide Orderid"},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "flag" not in data:
            return Response({"error":"Provide flag"},status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            objj = Order.objects.get(id = data["orderid"])

        except(ObjectDoesNotExist):
            return Response({"error":"Object does not exist please cheak"})
            
        try:
            invoice = Invoice.objects.filter(order=objj).first()
        except:
            invoice = None
        
        if data["flag"] == "payment_done":
            objj.is_payment_done = True
            objj.save()
            if invoice is not None:
                if objj.billing_option == 'CASH_ON_DELIVERY':
                    invoice.status = "CASH_ON_DELIVERY"
                else:
                    invoice.status = "PAID"
                invoice.save()
            return self.get(request)
        else:
            return Response({"error":"You Provide wrong flag on wrong url please cheak"})
        
    def delete(self,request,pk):

        try:
            obj = Order.objects.get(id = pk)
        except(ObjectDoesNotExist):
            return Response({"error":"Not found Object Data"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
        try:
            invoice = Invoice.objects.filter(order=objj).first()
        except:
            invoice = None
            
        if invoice is not None:
            invoice.status = "DELETED"
            invoice.save()
        obj.is_cancel  = True
        obj.save()

        return self.get(request)



class ActiveOrderManagement(APIView):
    permission_classes = [IsOrderManager]
    def get(self,request):
        objj = Order.objects.filter(is_served = False,is_payment_done=True,is_cancel = False)
        ser = OrderSerializer(objj,many = True)

        return Response(ser.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        data = request.data 
        if "orderid" not in data:
            return Response({"error":"Provide Orderid"},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "flag" not in data:
            return Response({"error":"Provide flag"},status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            objj = Order.objects.get(id = data["orderid"])

        except(ObjectDoesNotExist):
            return Response({"error":"Object does not exist please cheak"})
        
        items = OrderItem.objects.filter(order = objj)
        total_product_price = 0
        for i in items:
            total_product_price+= i.price
        
        inv = Invoice.objects.filter(order=objj).first()
        if data["flag"] == "served_done":
            objj.is_served = True
            objj.save()
            send_mail(
            "Your Order Details from Robomartbd",
            "You ordered something",
            "robomartbd@gmail.com",
            [objj.user.email],
            fail_silently= False,
            html_message=render_to_string('email.html',{'order':objj,'items':items,'product_price':total_product_price,'invoice':inv})
            )
            return self.get(request)
        else:
            return Response({"error":"You Provide wrong flag on wrong url please cheak"})
    



class ServedOrderManagement(APIView):
    permission_classes = [IsOrderManager]
    def get(self,request):
        objj = Order.objects.filter(is_served = True,is_payment_done=True,is_sell_done = False,is_cancel = False)
        ser = OrderSerializer(objj,many = True)

        return Response(ser.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        data = request.data 
        if "orderid" not in data:
            return Response({"error":"Provide Orderid"},status=status.HTTP_406_NOT_ACCEPTABLE)
        if "flag" not in data:
            return Response({"error":"Provide flag"},status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            objj = Order.objects.get(id = data["orderid"])

        except(ObjectDoesNotExist):
            return Response({"error":"Object does not exist please cheak"})
        
        if data["flag"] == "sell_done":
            objj.is_sell_done = True
            objj.save()

            order_item = OrderItem.objects.filter(order = objj)
            total_profit = 0
            for i in order_item:
                total_profit += (i.price - (i.product.buying_price * i.quantity) )

            sell = Sell(order = objj,total_price = objj.total_price,total_profit = total_profit)
            sell.save()
            return self.get(request)
        else:
            return Response({"error":"You Provide wrong flag on wrong url please cheak"})
        
    def delete(self,request,pk):

        try:
            obj = Order.objects.get(id = pk)
        except(ObjectDoesNotExist):
            return Response({"error":"Not found Object Data"},status=status.HTTP_406_NOT_ACCEPTABLE)
        obj.is_cancel = True
        obj.save()
        
        try:
            invoice = Invoice.objects.filter(order=objj).first()
        except:
            invoice = None
            
        if invoice is not None:
            invoice.status = 'DELETE'
            invoice.save()

        return self.get(request)
    
        
class DashbordData(APIView):
    permission_classes = [AdminPermission]
    def get(self,request):
        current_date = datetime.now()
        total_sell = 0
        total_profit = 0
        objj = Sell.objects.all()

        for i in objj:
            orderitems = OrderItem.objects.filter(order = i.order)
            total_sell+=orderitems.count()
            total_profit+=i.total_profit

        total_order = Order.objects.all().count()
        active_order = Order.objects.filter(is_served = False,is_payment_done=True).count()
        pending_order = Order.objects.filter(is_payment_done=False).count()
        completed_order = Order.objects.filter(is_sell_done = True).count()
        success = (completed_order*100)/total_order

        current_month_sell  = Sell.objects.filter(date__month = current_date.month, date__year = current_date.year)
        current_month_total_sell = 0
        current_month_total_profit = 0
        for i in current_month_sell:
            orderitems = OrderItem.objects.filter(order = i.order)
            current_month_total_sell+=orderitems.count()
            current_month_total_profit+=i.total_profit

    
        objj = AdminPage(total_order= total_order, active_order = active_order, pending_order=pending_order, completed_order= completed_order,success= success,current_month_sell = current_month_total_sell,current_month_profit = current_month_total_profit,total_sell = total_sell,total_profit =total_profit)
        ser = AdminPageSerializer(objj)
        return Response(ser.data,status=status.HTTP_200_OK)


class DashbordDataYearly(APIView):
    permission_classes = [AdminPermission]
    def post(self,request):
        current_date = datetime.now()
        print(current_date.month)
        data = request.data 
        if "year" not in data:
            return Response({"error":"Provide A year"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        array = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        object_sell_array = []

        objj = Sell.objects.filter(date__year = data["year"])
        for i in range(1,13):

            data = objj.filter(date__month = i)
            this_month_sell = 0
            this_month_profit = 0
            if data.exists():
                for j in data:
                    this_month_sell+= j.total_price
                    this_month_profit+=j.total_profit

            o = YearlySellReport(month=array[i],sell=this_month_sell,profit=this_month_profit)
            object_sell_array.append(o)
        
        ser = YearlySellReportSerializer(object_sell_array,many = True)
        return Response(ser.data,status=status.HTTP_201_CREATED)
        
        
class savecontact(APIView):
    
    def post(self,request):
        data = request.data
        
        if 'name' not in data:
            return Response({"msg":"Please Provide Name "}, status = status.HTTP_406_NOT_ACCEPTABLE)
            
        if 'email' not in data:
            return Response({"msg":"Please Provide Email "}, status = status.HTTP_406_NOT_ACCEPTABLE)
            
        if 'msg' not in data:
            return Response({"msg":"Please Provide msg "}, status = status.HTTP_406_NOT_ACCEPTABLE)
            
        objj = Contact.objects.create(name = data['name'], email = data['email'], msg = data['msg'])
        
        objj.save()
        
        return Response({'msg':'Done!'}, status = status.HTTP_201_CREATED)


# def renderhtml(request):
#     objj = Order.objects.get(id=33)
#     items = OrderItem.objects.filter(order = objj)
#     send_mail(
#             "Your Order Details from Robomartbd",
#             "You order something",
#             "roy35-909@diu.edu.bd",
#             ['souravkumarroy77@gmail.com'],
#             fail_silently= False,
#             html_message=render_to_string('email.html',{'order':objj,'items':items})
#         )
#     return render(request,'email.html',context={'order':objj,'items':items})
