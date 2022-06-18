from typing_extensions import Required
from rest_framework import serializers
from .models import Product
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(max_length=200,required=True)
    product_description=serializers.CharField(max_length=200,required=True)
    price=serializers.IntegerField(required=True)
    product_review=serializers.IntegerField(required=True)
    

    # def validate(self, data):
    #     print(data['name'])
    #     for i in data['name']:
    #         if i.isdigit():
    #             raise serializers.ValidationError("name should not be digit")

    #     if (len(str(data['phone_number']))<10 or len(str(data['phone_number']))>10):
    #         raise serializers.ValidationError("Phone number should be 10 digits")

    #     return data

    



    class Meta:
        model = Product
        fields = '__all__'
