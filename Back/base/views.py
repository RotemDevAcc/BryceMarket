from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth.models import User
# from .models import UserProfile, Product, Category, Receipt
from .models import MarketUser, Product, Category, Receipt
from .serializer import ProductSerializer, CategorySerializer, ReceiptSerializer
# from .serializer import UserSerializer, ProductSerializer, CategorySerializer, ReceiptSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
import json
from decimal import Decimal


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff or None

        # ...
 
        return token
 
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#def is_user_admin(user):
    #if not user or user == None:
        #return
    
    #print(is_user_admin(request.user))

    #return user.is_staff

def index(req):
    return Response('hello', safe=False)



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
            user_instance = MarketUser.objects.get(username=user)

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

# Management
@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(["GET"])
def receipts(request):
    user = request.user
    #if not is_user_admin(user):
        #return Response({"state":"fail","msg":"ERROR 401"})
    
    receipts = Receipt.objects.all()
    products = Product.objects.all()
    product_serializer = ProductSerializer(products, many=True)  # Use the serializer
    allproducts = product_serializer.data  # Retrieve the serialized data
    payload = []
    for receipt in receipts:

        try:
            recuser = MarketUser.objects.get(id=receipt.user_id)
            products_list = json.loads(receipt.products)
            payload.append({
                "id": receipt.id,
                "price": receipt.price,
                "products": products_list,
                "recuser": {"userid": recuser.id, "username": recuser.username}
            })
        except MarketUser.DoesNotExist:
            return Response({"state": "fail", "msg": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"state":"success","payload":payload,"products":allproducts,"msg":"Success"})

@permission_classes([IsAuthenticated, IsAdminUser])
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
    
@permission_classes([IsAuthenticated, IsAdminUser])
class PManagemetView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """
    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        categories = Category.objects.all()
        serializer2 = CategorySerializer(categories, many=True)

        merged_data = {
            "products": serializer.data,
            "categories": serializer2.data,
        }

        return Response(merged_data)


    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        reqtype = request.data.get('type')
        if not reqtype or reqtype == None:
            return Response({"success": False, "message": f"Request Failed"})
        
        if reqtype == "product":
             
            serializer = ProductSerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                image_file = request.data.get('img')
                
                if image_file:
                    # Check file format and size
                    allowed_formats = ['.png']
                    max_size = 2 * 1024 * 1024  # 2MB
                    
                    if not image_file.name.lower().endswith(tuple(allowed_formats)):
                        raise ValidationError("Please upload a PNG image.")
                    
                    if image_file.size > max_size:
                        raise ValidationError("Image size must be less than 2MB.")
                    
                    request.data['img'] = SimpleUploadedFile(image_file.name, image_file.read())
                    
                serializer.save()
                return Response({"success": True, "message": f"The Product Was Added Successfully"})
                #return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"success": False, "message": f"The Product couldn't be added"})
        elif reqtype == "category":
            serializer = CategorySerializer(data=request.data, context={'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "message": f"The Product Was Added Successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk):
        """
        Handle PUT requests to update an existing product
        """
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            # Handle the uploaded image file
            image_file = request.data.get('image')
            
            if image_file:
                # Check file format and size
                allowed_formats = ['.png']
                max_size = 2 * 1024 * 1024  # 2MB
                
                if not image_file.name.lower().endswith(tuple(allowed_formats)):
                    raise ValidationError("Please upload a PNG image.")
                
                if image_file.size > max_size:
                    raise ValidationError("Image size must be less than 2MB.")
                
                product.img = SimpleUploadedFile(image_file.name, image_file.read())

            serializer.save()
            # return Response(serializer.data)
            return Response({"success":True,"message":f"Product {product.name} Has been updated successfully"})
    
        return Response({"success":False,"message":"The Product was not found."})
   
    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            
            # Check if the product's image is not the default placeholder
            if product.img.name != '/placeholder.png':
                # Delete the image file from storage
                default_storage.delete(product.img.name)

            product.delete()
            return Response({"success": True, "message": f"Product {pk} Was Deleted Successfully"})
        except Product.DoesNotExist:
            return Response({"success": False, "message": f"Product {pk} not found"})
        

@permission_classes([AllowAny])
class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        gender = data.get('gender')
        date_of_birth = data.get('date')

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({'success': False, 'message': str(e)}, status=400)

        user = MarketUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            gender=gender,
            date_of_birth=date_of_birth
        )

        return Response({'success': True, 'message': 'Registration successful'})
    

from django.core.mail import send_mail

@permission_classes([AllowAny])
@api_view(["POST"])
def recovery(request):
    data = json.loads(request.body)
    email = data.get('email')
    try:
        user = MarketUser.objects.get(email=email)
        YOUR_RESET_URL = ""
        # Generate a unique token for password reset
        # You can use a library like Django Rest Framework's default token generator
        # or implement your own logic to generate a secure token
        reset_token = generate_reset_token(user)

        # Send an email with a link to the password reset view
        subject = 'Password Reset'
        message = f'Click the following link to reset your password: {YOUR_RESET_URL}?token={reset_token}'
        from_email = 'guyron2000@gmail.com'  # Update with your email
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return Response({'success': True, 'message': f'Password Recovery Sent To {email}'})
    except MarketUser.DoesNotExist:
        #return Response({"success": False, "message": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        # Pretending we sent the email so that the client won't use this information against us
        return Response({'success': True, 'message': f'Password Recovery Sent To {email}'})
    except ValidationError as e:
        print(str(e))
        return Response({'success': False, 'message': "Something Went Wrong"}, status=400)
    
def generate_reset_token(user):
    # Implement your logic to generate a secure token
    # You can use Django Rest Framework's default token generator or other methods
    return 'your_generated_token'

@permission_classes([IsAuthenticated])
@api_view(["POST"])
def modprofile(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ruser = request.user
        rtype = data.get('rtype')
        if rtype == "picture":
            user = MarketUser.objects.get(id=user.id)
            print(user.id)
            if ruser.id != user.id:
                return Response({"success":False,'message':"Something Went Wrong(1)"})

            return Response({"success":True,'message':"Picture Changed Successfully"})
        else:
            return Response({"success":False,'message':"Something Went Wrong(2)"})
            
