from rest_framework import serializers
from .models import Brand,Phone


class PhoneSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name',read_only=True)

    class Meta:
        model = Phone
        fields = ['id','brand','brand_name','model_name','price','stock']

class BrandSerializer(serializers.ModelSerializer):
    phones = PhoneSerializer(many=True,read_only=True)

    class Meta:
        model = Brand
        fields = ['id','name','phones']