
from django.urls import path,include
from .views import *
urlpatterns = [
    
    path('catagorylist', CatagoryList.as_view() ),
    path('home',HomepageView.as_view()),
    path('catagory/<int:pk>/<str:flag>', GetCatagoryProducts.as_view()),
    path('product/<int:pk>', GetProduct.as_view()),
    path('products', ProductSrc.as_view()),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('auth/',include('djoser.social.urls')),
    path('our_client',CorporateClient.as_view()),
    path('our_supplier',OurSupplier.as_view()),
    path('profile',Profile.as_view()),
    path('test',PostView.as_view()),
    path('change_password',ChangePassword.as_view()),
    path('renew_password/<str:email>/<str:token>',RenewPassword.as_view()),
    # path("dj-rest-auth/google/login/", GoogleLoginView.as_view(), name="google_login")
    
]
