from tabnanny import check
from unicodedata import name
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
    def get(self, request):
            #If name exists in database
        # if Contact.objects.filter(name=name).first():
        #     item = Contact.objects.get(name=name)
        #     serializer = ProductSerializer(item)
        #     return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        #     #If the name does not exists in data base
        # else:
        #     return Response({"error": "Name not found"})
            
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
