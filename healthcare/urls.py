from django.urls import path
from healthcare.views import ProductList


urlpatterns=[
    path('products/',ProductList.as_view(),name='contacts')
]