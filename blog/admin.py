from django.contrib import admin
from .models import Blog,Comment,Pages,BlogTag,BlogCategory,BlogItems
from froala_editor.widgets import FroalaEditor
class PageInline(admin.TabularInline):
    #content = admin.CharField(widget=FroalaEditor)
    model = Pages
    extra = 1
    class Media:
        js = ['code_insert.js']
        css={'all':['code.css']}
        
class ItemInline(admin.TabularInline):
    #content = admin.CharField(widget=FroalaEditor)
    model = BlogItems
    extra = 0
        

class BlogAdmin(admin.ModelAdmin):
    inlines=[PageInline,ItemInline]
    class Meta:
        model = Blog







admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogItems)
admin.site.register(Comment)
admin.site.register(Pages)
admin.site.register(BlogCategory)
admin.site.register(BlogTag)