from django.db import models

from Basic_Api.models import User,Product
from froala_editor.fields import FroalaField
from froala_editor.widgets import FroalaEditor



class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Blog_Category/',null=True,blank=True)
    def __str__(self) -> str:
        return self.name
    
class BlogTag(models.Model):
    tag_name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.tag_name
    

    

class Blog(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000,verbose_name="Write Your Description")
    related_Product = models.ManyToManyField(Product,null=True,blank=True)
    is_tutorial = models.BooleanField(default=False)
    image = models.ImageField(upload_to='Blog/',null=True,blank=True)
    category = models.ManyToManyField(BlogCategory)
    tag = models.ManyToManyField(BlogTag)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} by {self.created_by.first_name} {self.created_by.last_name}"


class BlogItems(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self) -> str:
        return self.product.name

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
    

class Pages(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    page_no = models.IntegerField()
    # page title
    page_title = models.CharField(max_length=255,null=True,blank=True)
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
    content = MyFroalaField(null=True,blank = True,**op)
    

class Comment(models.Model):
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    reply = models.TextField(max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog.title} by {self.commented_by.first_name}"


