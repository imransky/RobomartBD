from django.urls import path
from .views import *
urlpatterns = [
    
 path('get_order',GetOrder.as_view()),
 path('cheak_copun',CheakCupon.as_view()),
    
]
