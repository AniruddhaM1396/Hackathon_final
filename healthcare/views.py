from tabnanny import check
from unicodedata import name
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from numpy import product
from .models import Product, Appuser
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class ProductList(APIView):
    # Fuction to get all the contacts that are present in the database. This function is also used to find data of particular user by name.
    def get(self, request, product_name=None):
            #If name exists in database
        if product_name:
            if Product.objects.filter(product_name=product_name).first():
                item = Product.objects.get(product_name=product_name)
                serializer = ProductSerializer(item)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                #If the name does not exists in data base
            else:
                return Response({"error": "Product not found"})
            
        items = Product.objects.all()
        serializer = ProductSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class ProductSave(APIView):
    #Function to post the data of a contact. Validation part is done in the Serializers.py
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        #serialiser.is_valid does the required validation 
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdate(APIView):
    #This function marks a contact as spam.
    def post(self,request):
        product_name=request.data.get("product_name")
        product_desc=request.data.get("product_description")
        print(product_desc)
        #IF phone number field is empty
        if product_name is None:
            return Response({"Error": "product name required"}, status=status.HTTP_400_BAD_REQUEST)

        product=Product.objects.filter(product_name=product_name).update(product_description=product_desc)
        #Successfully marked as spam
        if (product):
            return Response({"Success": "product details updated "}, status=status.HTTP_200_OK)
        #Phone number not found in Database
        else:
            return Response({"Error":"product name not found"},status = status.HTTP_404_NOT_FOUND)
