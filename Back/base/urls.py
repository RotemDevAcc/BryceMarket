from django.urls import path, include
from . import views
from .views import ProductsView, PManagemetView
urlpatterns = [
    path('', views.index),
    path('products/', ProductsView.as_view(), name='product-list'),
    path('productslist/',views.productlist),
    path('getreceipts/', views.receipts),
    path('login/', views.TokenObtainPairView.as_view()),
    path('pmanagement/', PManagemetView.as_view(), name='product-manage'),
    path('pmanagement/<int:pk>/', PManagemetView.as_view(), name='product-managepk'),

    # path('purchase/',views.purchase)
]
