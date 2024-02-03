from rest_framework import serializers
from django.db.models import QuerySet
from Basic_Api.models import User
from rest_framework.fields import empty
from .models import Product,Catagory,Homepage,Homeslider,Spacialoffer,SubCatagory,OurClient,Supplier,ProductMedia
from djoser.serializers import UserCreateSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework.settings import api_settings
from django.contrib.auth import authenticate, get_user_model

class UserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id','email','first_name','last_name','password','balance','phone',)

    def update(self, instance, validated_data):
        # Somehow save instance with new quiz_data
        print(validated_data)
        return instance
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name',)



class HomesliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homeslider
        fields = '__all__'
class SpacialofferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homeslider
        fields = '__all__'
class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','photo','discription',)

class HomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homepage
        fields = '__all__'
    homeslider = serializers.SerializerMethodField()
    spacialoffer = serializers.SerializerMethodField()
    catagory = serializers.SerializerMethodField()
    catagorylist = serializers.SerializerMethodField()

    def get_homeslider(self,obj):
        homeslider = Homeslider.objects.filter(isactive = True)
        homeslider_serializer = HomesliderSerializer(homeslider,many = True, context={'request':self.context.get('request')})

        return homeslider_serializer.data
    
    def get_spacialoffer(self,obj):
        spacialoffer = Spacialoffer.objects.filter(isactive = True)
        spacialoffer_serializer = SpacialofferSerializer(spacialoffer,many = True, context={'request':self.context.get('request')})
        return spacialoffer_serializer.data
    
    def get_catagory(self,obj):
        catagory = Catagory.objects.filter(show_on_home = True)
        product_serializer = CatagorySerializer(catagory,many = True, context={'request':self.context.get('request')})
        return product_serializer.data
    def get_catagorylist(self,obj ):
        catagorylist = Catagory.objects.all()
        catagorylist_serializer = CatagoryListSerializer(catagorylist,many = True, context={'request':self.context.get('request')})
        return catagorylist_serializer.data



class ProductSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('catagorys','after_discount','colors','stock','total_review','sub_catagory',)


class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
    def get_media(self,instance):
        obj = ProductMedia.objects.filter(product = instance)
        ser = ProductMediaSerializer(obj,many=True, context={'request':self.context.get('request')})
        return ser.data


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= SubCatagory
        fields = ["id","name","image"]

class CatagoryListSerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = Catagory
        fields = ["id","name","sub_category"]

    def get_sub_category(self,instance):
        sub = SubCatagory.objects.filter(category=instance)
        if sub.exists():
            ser = SubCategorySerializer(sub,many=True, context={'request':self.context.get('request')})
            return ser.data
        else:
            return None


class CatagorySerializer(serializers.ModelSerializer):
    #product = ProductSerializerList(source="product_set",many=True,read_only=True)
    product = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    def get_product(self, obj):
        categories = obj.product_set.all() 
        sub_cata = SubCatagory.objects.filter(category = obj)
        data = []
        if sub_cata.exists():
            for i in sub_cata:
                o = i.product_set.all()
                ser_data = ProductSerializerList(o,many=True,context={'request':self.context.get('request')})
                data+=ser_data.data
        
        category_serializer = ProductSerializerList(categories, many=True, context={'request':self.context.get('request')})
        data+=category_serializer.data
        return data[:7]
    class Meta:
        model = Catagory
        fields = ["id","name","image","product","sub_category"]
    def get_sub_category(self,instance):
        sub = SubCatagory.objects.filter(category=instance)
        if sub.exists():
            ser = SubCategorySerializer(sub,many=True, context={'request':self.context.get('request')})
            return ser.data
        else:
            return None


class OurCorporateClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OurClient

        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier

        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("first_name","last_name","balance","address","email","phone","role",)

    def get_role(self,instance):

        if instance.is_superuser or instance.is_staff:
            return "Admin"
        else:
            return "Customer"
        
