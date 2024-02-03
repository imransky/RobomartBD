from django.urls import path
from .views import *
urlpatterns = [
    
 path('<int:pk>/get_all_comment',GetAllComment.as_view()),
 path('get_comment',GetComment.as_view()),
 path('get_blog',GetAllBlog.as_view()),
 path('get_tutorial',GetAllTutorial.as_view()),
 path('get_blog/<int:pk>',GetBlog.as_view()),
 path('get_all_blog_by_category/<int:pk>',GetBlogByCategory.as_view()),
 path('get_all_blog_by_tag/<int:pk>',GetBlogByTag.as_view()),
 path('get_all_tag',GetTag.as_view()),
 path('get_all_category',GetCategory.as_view()),
    
]
