from rest_framework import serializers
# from .models import UserProfile,Product,Category, Receipt
from .models import MarketUser,Product,Category, Receipt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketUser
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