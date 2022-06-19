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

@permission_classes((AllowAny,))
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


@permission_classes((AllowAny,))
class RegisterApp(APIView):
    #Function to register a User to the App. Uses name as the username.
    def post(self,request):
        user=request.data.get("user")
        print(user)
        phone_number=request.data.get("phone_number")
        print(phone_number)
        #If name or Phone is not provided
        if user is None or phone_number is None:
            return Response({"Error":"Both name and phone_number are required"}, status = status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username = request.data["user"]).first():
            return Response({"Error":"Username already taken"}, status = status.HTTP_400_BAD_REQUEST)
            
        try:
            if request.data["email"]:
                email = request.data["email"]
                print("email:",email)
        except:
            email="NONE"
        user=User(
				username=request.data["user"],
				password=request.data["password"],
				email=email,
			)
        if user:
            user.set_password(request.data["password"])
            print("user data",user)
            user.save()
            profile=Appuser.objects.create(
	        		user=user,
	        		phone_number=request.data["phone_number"],
	        		email=email,
	        	)
            username=request.data.get("user")
            password=request.data.get("password")
            print("username:",username)
            print("password:",password)
            user = authenticate(username = username, password = password)
            print('user:',user)
            token, _ =Token.objects.get_or_create(user = user)
            return Response({"Token":token.key},status=status.HTTP_200_OK)
            #return Response({"Message":"Registered to App successfully"},status = status.HTTP_200_OK)
        else:
            return Response({"Message":"Try again with different Username/Password"},status = status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny,))
class GetToken(APIView):
    #Function generates a token for the Registered user once he provides the username and password.
    def post(self,request):
        #when a empty body is posted
        if not request.data:
            return Response({"Error":"Please provide username/password"},status=status.HTTP_400_BAD_REQUEST)
        
        username=request.data.get("username")
        password=request.data.get("password")
        #WHen either Username or Password is empty
        if username is None or password is None:
            return Response({"Error":"Invalid Credentials"},status=status.HTTP_404_NOT_FOUND)

        #If username does not exist in the database
        if not User.objects.filter(username = username).first():
            return Response({"Error":"Username does not exist in database"}, status = status.HTTP_400_BAD_REQUEST)
         
        #successfully create a token
        try:
            user = authenticate(username = username, password = password)
            print('user:',user)
            token, _ =Token.objects.get_or_create(user = user)
            return Response({"Token":token.key},status=status.HTTP_200_OK)

        except:
            return Response({"Error":"Password does not match"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
