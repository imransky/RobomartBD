from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,AbstractUser
#custom user manager
from froala_editor.fields import FroalaField
from froala_editor.widgets import FroalaEditor
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email is required..')
        email = self.normalize_email(email)
        user = self.model(email = email,**extra_fields)
        
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        return self.create_user(email=email,password=password,**extra_fields)

#Custom User Model
class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.IntegerField(default=0)
    balance_ref = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=18,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    password_forget_token = models.CharField(max_length=255,null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    # def __str__(self) -> str:
    #     return self.email
    # def has_perm(self,perm,obj=None):
    #     return self.is_admin
    # def has_module_perms(self,app_label):
    #     return True
    # def get_full_name(self):
    #     return self.first_name+' '+self.last_name

    # @property
    # def is_staff(self):
    #     return self.staff
    # @property
    # def is_superuser(self):
    #     return self.is_admin
    objects = UserManager()


class MyFroalaEditor(FroalaEditor):
    def trigger_froala(self, el_id, options):

        str = """
        <script>
        FroalaEditor.DefineIcon('insertCodeBlock', {
        NAME: 'code',
        SVG_KEY: "codeView",
        });
        FroalaEditor.RegisterCommand ('insertCodeBlock', {
        title: 'Insert Code',
        icon: 'insertCodeBlock',
        focus: true,
        undo: true,
        refreshAfterCallback: true,
        callback: function () {
          // Insert the code section where the cursor is
          this.html.insert('<div class="code_area"><pre><code> </code></pre></div></br>');
          this.event.focus();
        },
      });
            new FroalaEditor('#%s',%s)
        </script>""" % (el_id, options)
        return str


class MyFroalaField(FroalaField):

    def __init__(self, *args, **kwargs):
        super(MyFroalaField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if self.use_froala:
            widget = MyFroalaEditor(options=self.options, theme=self.theme, plugins=self.plugins,
                                  image_upload=self.image_upload,
                                  file_upload=self.file_upload, third_party=self.third_party)

        defaults = {'widget': widget}
        defaults.update(kwargs)
        return super(FroalaField, self).formfield(**defaults)

    

class Homepage(models.Model):
    key = models.IntegerField(blank=True,null=True)
    logo = models.ImageField()
    shop_poster = models.ImageField()
    phone = models.CharField(max_length=15)
    facebook = models.CharField(max_length=200)
    youtube = models.CharField(max_length=200)
    linkdin = models.CharField(max_length=200)
    twiter = models.CharField(max_length=200)
    instragram = models.CharField(max_length=200)

class Homeslider(models.Model):
    isactive = models.BooleanField(default=True)
    poster = models.ImageField()
    link = models.URLField(null=True,blank=True)

class Spacialoffer(models.Model):
    isactive = models.BooleanField(default=True)
    poster = models.ImageField()
    link = models.URLField(null=True,blank=True)


class Catagory(models.Model):
    name = models.CharField(max_length=200)
    show_on_home = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(upload_to='CategoryImage/',null=True,blank=True)
    def __str__(self) -> str:
        return self.name

class SubCatagory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Catagory,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='SubCategoryImage/',null=True,blank=True)
    def __str__(self):
        return self.name

class Product(models.Model):

    op = {'options':{
    
    "toolbarButtons": [[
            "bold",
            "italic",
            "underline",
            "strikeThrough",
            "subscript",
            "superscript",
          ], [
            "fontFamily",
            "fontSize",
            "textColor",
            "backgroundColor",
            "inlineStyle",
            "paragraphStyle",
            "paragraphFormat",
            
          ],["align", "formatOL", "formatUL", "outdent", "indent",],"-",["insertLink", "insertImage", "insertVideo","insertCodeBlock"],["undo", "redo","fullscreen"],],


    "icons" : {"insertCodeBlock":"<i class=\"fa fa-code\"></i>"}
  }}
    
    name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=200,null=True,blank=True)
    price = models.IntegerField(verbose_name= "Final Price")
    discount = models.IntegerField()
    after_discount = models.IntegerField(verbose_name="Regular Price")
    photo = models.ImageField(null=True,blank=True)
    discription = models.TextField(max_length=500)
    ratting = models.DecimalField(max_digits=5, decimal_places=2)
    colors = models.CharField(max_length=255)
    stock = models.IntegerField()
    total_review = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    catagorys = models.ManyToManyField(Catagory,null=True,blank=True)
    sub_catagory = models.ManyToManyField(SubCatagory,null=True,blank=True)
    buying_price = models.IntegerField(null=True,blank=True)
    product_discription = MyFroalaField(null = True, blank = True , **op)
    product_tutorial = MyFroalaField(null = True, blank = True , **op)

    def __str__(self) -> str:
        return self.name


class ProductMedia(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='All_Product_Additional_Photo/')

    def __str__(self) -> str:
        return self.product.name





class Review(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    r_name = models.CharField(max_length=500)
    review = models.TextField(max_length=3000)
    date = models.DateField(auto_now_add=True,null=True,blank=True)
    def __str__(self) -> str:
        return self.r_name




class Cupon(models.Model):
    cupun_code = models.CharField(max_length=200,unique=True)
    offer_name = models.CharField(max_length=500)
    price_condition = models.IntegerField()
    discount_in_percentage = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.offer_name
    




class OurClient(models.Model):
    name = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='OurClient/',null=True,blank=True)
    link = models.URLField()

    def __str__(self) -> str:
        return self.name
    

class Supplier(models.Model):
    name = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='OurSupplier/',null=True,blank=True)
    link = models.URLField()

    def __str__(self) -> str:
        return self.name
    