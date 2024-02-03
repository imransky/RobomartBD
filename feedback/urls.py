from django.urls import path
from .views import *
urlpatterns = [
    
 path('get_all_feedback/<int:pk>',GetAllFeedback.as_view()),
 path('get_feedback',GetFeedback.as_view()),
    
]
