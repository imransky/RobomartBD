from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
class GetFeedback(APIView):
    permission_classes = [IsAuthenticated]
    #Get a User All Feedback
    def get(self,request,format = None):
        obj = Feedback.objects.filter(user=request.user)
        ser = FeedbackSerializer(obj,many = True)
        return Response(ser.data)
    # Create a Feedback Of a Product
    def post(self,request,format = None):
        data = request.data

        if 'product' not in data:
            return Response({'error': 'did you give product id ?'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if 'review' not in data:
            return Response({'error': 'did you give review?'},status=status.HTTP_406_NOT_ACCEPTABLE)
        if 'ratting' not in data:
            return Response({'error': 'did you ratting ?'},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        try:
            product = Product.objects.get(id = data['product'])
        except(ObjectDoesNotExist):
            return Response({'error': 'did you give valid product id ?'},status=status.HTTP_404_NOT_FOUND)
        obj = Feedback(user=request.user,product=product,ratting=data['ratting'],review=data['review'])
        obj.save()
        obj_ser = FeedbackSerializer(obj)
        return Response(obj_ser.data,status=status.HTTP_201_CREATED)
    # Delete A feedback of this User and His Created Feedback
    def delete(self,request,format = None):
        data = request.data
        if 'feedback' not in data:
            return Response({'error': 'did you give  feedback id ? '},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        try:
            feedback = Feedback.objects.get(id=data['feedback'])
        except(ObjectDoesNotExist):
            return Response({'error': 'did you give valid feedback id ?'},status=status.HTTP_404_NOT_FOUND)
        if feedback.user== request.user:
            feedback.delete()
            return Response({"Success":"Successfully Deleted"},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"Error": "You are not creator of this Feedback"},status=status.HTTP_401_UNAUTHORIZED)
        
#Get All FeedBack  
class GetAllFeedback(APIView):
    permission_classes = []
    def get(self,request,pk,format = None):
        try:
            product = Product.objects.get(id=pk)
        except(ObjectDoesNotExist):
            return Response({'error': 'The Product Does not exist?'},status=status.HTTP_404_NOT_FOUND)
        obj = Feedback.objects.filter(product=product)
        ser = FeedbackSerializer(obj,many = True)
        return Response(ser.data,status=status.HTTP_200_OK)

  

"""
    def delete(self,request,format = None):
        data = request.data
        product = Product.objects.get(id=data['product'])
        obj = Cart.objects.get(user = request.user)
        obj.products.remove(product)
        obj.count = obj.products.all().count()
        obj.save()
        ser = CartSerializerList(obj)
        return Response(ser.data)
"""


