from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

class BasicPagination(PageNumberPagination):
    page_size_query_param = '1'
    page_size=10
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.num_pages,
            'results': data
        })


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
    def paginate_queryset(self, queryset):
        
        if self.paginator is None:
            
            return None
        res = self.paginator.paginate_queryset(queryset,self.request, view=self)
        print(self.paginator)
        return res
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class GetComment(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format = None):
        obj = Comment.objects.filter(commented_by=request.user)  
        ser = CommentSerializer(obj,many = True,context={'request':request})
        return Response(ser.data)

    def post(self,request,format = None):
        data = request.data
        blog = Blog.objects.get(id = data['blog'])
        obj = Comment(commented_by=request.user,blog=blog,comment=data['comment'])
        obj.save()
        obj_ser = CommentSerializer(obj,context={'request':request})
        return Response(obj_ser.data)
    
    def delete(self,request,format = None):
        data = request.data
        comment = Comment.objects.get(id=data['comment'])
        if comment.commented_by== request.user:
            comment.delete()
            return Response({"Success":"Successfully Deleted"})
        else:
            return Response({"Error": "You are not creator of this Comment"})
       
    
class GetAllComment(APIView):
    permission_classes = []
    def get(self,request,pk,format = None):
        
        try:
            blog = Blog.objects.get(id=pk)
        except(ObjectDoesNotExist):
            return Response({'error':'Blog not found by this id'})
        obj = Comment.objects.filter(blog=blog)
        ser = CommentSerializer(obj,many=True,context = {'request':request})
        return Response(ser.data,status=status.HTTP_200_OK)



class GetAllBlog(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = BlogSerializer
    permission_classes = []

    def get(self,request,format = None, *args, **kwargs):
        blog = Blog.objects.filter(is_tutorial = False)
        page = self.paginate_queryset(blog)
        if page is not None:
            print("Roy")
            serializer = self.get_paginated_response(self.serializer_class(page,many=True,context={'request':request}).data)
        else:
            serializer = self.serializer_class(blog, many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class GetAllTutorial(APIView,PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = BlogSerializer
    permission_classes = []

    def get(self,request,format = None, *args, **kwargs):
        blog = Blog.objects.filter(is_tutorial = True)
        page = self.paginate_queryset(blog)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,many=True,context={'request':request}).data)
        else:
            serializer = self.serializer_class(blog, many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class GetBlog(APIView):
    permission_classes = []

    def get(self,request,pk,format = None):
        try:
            blog = Blog.objects.get(id=pk)
        except(ObjectDoesNotExist):
            return Response({'error':'Blog not found'},status=status.HTTP_404_NOT_FOUND)
        ser = BlogSerializer(blog,context = {'request':request})
        return Response(ser.data,status=status.HTTP_200_OK)
    
class GetBlogByCategory(APIView,PaginationHandlerMixin):
    permission_classes = []
    pagination_class = BasicPagination
    serializer_class = BlogSerializer
    def get(self,request,pk,format = None,*args, **kwargs):
        try:
            category = BlogCategory.objects.get(id=pk)
        except(ObjectDoesNotExist):
            return Response({'error':'Category Not Found by this id'},status=status.HTTP_404_NOT_FOUND)
        
        blog = Blog.objects.filter(category=category)
        page = self.paginate_queryset(blog)
        if page is not None:
            
            serializer = self.get_paginated_response(self.serializer_class(page,many=True,context={'request':request}).data)
        else:
            serializer = self.serializer_class(blog, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetCategory(APIView):
    permission_classes = []

    def get(self,request,format = None):
        try:
            category = BlogCategory.objects.all()
        except(ObjectDoesNotExist):
            return Response({'error':'Category Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        
        ser = BlogCategorySerializer(category,many=True,context = {'request':request})
        return Response(ser.data,status=status.HTTP_200_OK)
    
class GetTag(APIView):
    permission_classes = []

    def get(self,request,format = None):
        try:
            tag = BlogTag.objects.all()
        except(ObjectDoesNotExist):
            return Response({'error':'Tag Not Found'},status=status.HTTP_404_NOT_FOUND)
        
        
        ser = TagSerializer(tag,many=True,context = {'request':request})
        return Response(ser.data,status=status.HTTP_200_OK)
    
class GetBlogByTag(APIView,PaginationHandlerMixin):
    permission_classes = []
    pagination_class = BasicPagination
    serializer_class = BlogSerializer
    def get(self,request,pk,format = None,*args, **kwargs):
        try:
            tag = BlogTag.objects.get(id=pk)
        except(ObjectDoesNotExist):
            return Response({'error':'tag Not Found by this id'},status=status.HTTP_404_NOT_FOUND)
        
        blog = Blog.objects.filter(tag=tag)
        page = self.paginate_queryset(blog)
        if page is not None:
            
            serializer = self.get_paginated_response(self.serializer_class(page,many=True,context={'request':request}).data)
        else:
            serializer = self.serializer_class(blog, many=True,context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)