from rest_framework import serializers
from django.db.models import QuerySet
from rest_framework.fields import empty
from .models import Comment,Blog,Pages,BlogCategory,BlogTag,BlogItems
from Basic_Api.serializers import UserCreateSerializer,ProductSerializerList

class CommentSerializer(serializers.ModelSerializer):
    commented_by = UserCreateSerializer(many=False)
    is_my_comment = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'

    def get_is_my_comment(self,instance):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if user!=None and instance.commented_by == user:
            return "true"
        else:
            return "false"

class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializerList()
    class Meta:
        model = BlogItems
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    created_by = UserCreateSerializer(many=False)
    related_Product = ProductSerializerList(many=True)
    pages = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = '__all__'

    def get_pages(self,instance):
        objj = Pages.objects.filter(blog = instance)

        ser = PagesSerializer(objj,many = True)
        return ser.data

    def get_items(self,instance):
        objj = BlogItems.objects.filter(blog=instance)
        ser = BlogItemsSerializer(objj,many=True, context={'request':self.context.get('request')})

        return ser.data


