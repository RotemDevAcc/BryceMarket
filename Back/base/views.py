from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product, Category
from .serializer import ProductSerializer, CategorySerializer, ReceiptSerializer
from django.core.exceptions import ObjectDoesNotExist
import json
from decimal import Decimal


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
 
        return token
 
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def is_user_admin(user):
    if not user or user == None:
        return
    
    #print(is_user_admin(request.user))

    return user.is_staff

def index(req):
    return JsonResponse('hello', safe=False)

@permission_classes([IsAuthenticated])
class ProductsView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):

        """
        Handle GET requests to return a list of MyModel objects
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """

        serializer = ProductSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@permission_classes([IsAuthenticated])
class CategoryView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """

        serializer = CategorySerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["GET","POST"])
def productlist(request):
    if not request.method: return
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        
        categories = Category.objects.all()
        serializer2 = CategorySerializer(categories, many=True)

        # Combine the serialized data into a single dictionary
        combined_data = {
            'products': serializer.data,
            'categories': serializer2.data,
        }
        return Response(combined_data)
    elif request.method == "POST":
        user = request.user
        price = Decimal(str(request.data['price']))
        cart = request.data['cart']
        totalPrice = Decimal('0')

        PurchasedItems = []

        for item_id, item_info in cart.items():
            try:
                product = Product.objects.get(id=item_info['id'])
                if product:
                    if product.price == Decimal(item_info['price']):
                        itemprice = Decimal(item_info['price'])
                        totalPrice += (itemprice * item_info['count'])
                        #PurchasedItems.append({"item": item_info['id'], "count": item_info['count'], "price": (itemprice * item_info['count']).quantize(Decimal('0.01'))})
                        PurchasedItems.append({
                            "item": item_info['id'],
                            "count": item_info['count'],
                            "price": float((itemprice * item_info['count']).quantize(Decimal('0.01')))
                        })
                    else:
                        print("Warning, Wrong Price")
                        return Response({"state": "fail", "msg": "ERROR, Something went wrong."})
                else:
                    print("Warning, Unauthorized Item Detected.")
                    return Response({"state": "fail", "msg": "ERROR, Something went wrong."})
            except ObjectDoesNotExist:
                print(f"Warning, Unauthorized Item Detected {item_info['id']}.")
                return Response({"state": "fail", "msg": "ERROR, Something went wrong."})

        if totalPrice == price:
            print("Purchase Completed")
            print(PurchasedItems)
            user_instance = User.objects.get(username=user)

            receipt_data = {
                'products': json.dumps(PurchasedItems),
                'price': float(totalPrice),
                'user': user_instance.id
            }

            serializer = ReceiptSerializer(data=receipt_data)
            if serializer.is_valid():
                serializer.save()
                print("Receipt saved successfully")
                return Response({"state": "success", "msg": f"Purchase Complete, You Bought All The Specificed Items For ${totalPrice}"})
            else:
                print("Error in data:", serializer.errors)
        else:
            print(f"Warning Wrong Price Client Reported: {type(price)}, Server Calculated: {type(totalPrice)}")
            print(f"Client Reported Price: {price}, Server Calculated Price: {totalPrice}")
            return Response({"state": "fail", "msg": "Purchase Failed"})

    

