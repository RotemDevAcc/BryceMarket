from rest_framework import serializers
from .models import UserProfile,Product,Category, Receipt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('__all__')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    
class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'products', 'price', 'user']