from django.urls import path
from .views import *
urlpatterns = [
    
path('get_active_order',ActiveOrderManagement.as_view()),
path('get_pending_order',PendingOrderManagement.as_view()),
path('get_pending_order/<int:pk>',PendingOrderManagement.as_view()),

path('get_order/<int:pk>',OrderDetails.as_view()),

path('post_contact',savecontact.as_view()),

path('get_served_order',ServedOrderManagement.as_view()),
path('get_served_order/<int:pk>',ServedOrderManagement.as_view()),
path('get_dashbord',DashbordData.as_view()),
path('get_dashbord_yearly',DashbordDataYearly.as_view()),
path('get_all_success_order',AllSuccessOrder.as_view()),
path('get_all_cancel_order',AllCancelOrder.as_view()),
# path('test_email', renderhtml),
#  path('cheak_copun',CheakCupon.as_view()),
    
]
