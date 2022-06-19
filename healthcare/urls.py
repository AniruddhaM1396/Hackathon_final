from django.urls import path
from healthcare.views import ProductList, ProductUpdate, RegisterApp, GetToken


urlpatterns=[
    path('products/',ProductList.as_view(),name='products'),
    path('products/<str:product_name>/',ProductList.as_view(),name='products'),
    path('updatedetails/',ProductUpdate.as_view(),name='update'),
    path('register/',RegisterApp.as_view(),name='register'),
    path('token/',GetToken.as_view(),name='token'),
]