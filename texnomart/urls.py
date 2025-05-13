from django.urls import path
from texnomart.views import (
    CategoryListCreateAPIView, CategoryDetailAPIView, CategoryProductsAPIView,
    ProductListCreateAPIView, ProductDetailAPIView,
    ProductImageListCreateAPIView, ProductImageDetailAPIView,
    ProductAttributeListCreateAPIView, ProductAttributeDetailAPIView,
    ProductPriceListCreateAPIView, ProductPriceDetailAPIView,
    ProductCommentListCreateAPIView, ProductCommentDetailAPIView,
    ProductCommentsAPIView,
    ProductRatingListCreateAPIView, ProductRatingDetailAPIView,
    LoginView, LogoutView
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/<int:pk>/products/', CategoryProductsAPIView.as_view(), name='category-products'),

    # Products
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/<int:pk>/comments/', ProductCommentsAPIView.as_view(), name='product-comments'),

    # Product Images
    path('images/', ProductImageListCreateAPIView.as_view(), name='image-list-create'),
    path('images/<int:pk>/', ProductImageDetailAPIView.as_view(), name='image-detail'),

    # Product Attributes
    path('attributes/', ProductAttributeListCreateAPIView.as_view(), name='attribute-list-create'),
    path('attributes/<int:pk>/', ProductAttributeDetailAPIView.as_view(), name='attribute-detail'),

    # Product Prices
    path('prices/', ProductPriceListCreateAPIView.as_view(), name='price-list-create'),
    path('prices/<int:pk>/', ProductPriceDetailAPIView.as_view(), name='price-detail'),

    # Product Comments
    path('comments/', ProductCommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', ProductCommentDetailAPIView.as_view(), name='comment-detail'),

    # Product Ratings
    path('ratings/', ProductRatingListCreateAPIView.as_view(), name='rating-list-create'),
    path('ratings/<int:pk>/', ProductRatingDetailAPIView.as_view(), name='rating-detail'),

    # Auth
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
