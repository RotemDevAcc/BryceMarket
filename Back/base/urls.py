from django.urls import path, include
from . import views
from .views import ProductsView, CategoryView
urlpatterns = [
    path('', views.index),
    path('categories/', CategoryView.as_view(), name='category-list'),
    path('products/', ProductsView.as_view(), name='product-list'),
    path('productslist/',views.productlist),
    path('login/', views.TokenObtainPairView.as_view()),
    # path('purchase/',views.purchase)
]
