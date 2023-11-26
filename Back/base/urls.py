from django.urls import path, include
from . import views
from .views import ProductsView, PManagemetView, RegistrationView
urlpatterns = [
    path('', views.index),
    path('products/', ProductsView.as_view(), name='product-list'),
    path('productslist/',views.productlist),
    path('getreceipts/', views.receipts),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('recovery/', views.recovery),
    path('register/', RegistrationView.as_view(), name='register'),
    path('pmanagement/', PManagemetView.as_view(), name='product-manage'),
    path('pmanagement/<int:pk>/', PManagemetView.as_view(), name='product-managepk'),

    # path('purchase/',views.purchase)
]
