import datetime
from django.core.cache import cache
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    Category, Product, ProductImage,
    ProductAttribute, ProductPrice,
    ProductComment, ProductRating
)
from .serializers import (
    CategorySerializer, ProductSerializer, ProductImageSerializer,
    ProductAttributeSerializer, ProductPriceSerializer,
    ProductCommentSerializer, ProductRatingSerializer
)


class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        key = "category_list"
        data = cache.get(key)
        if data:
            return data
        data = Category.objects.all()
        cache.set(key, data, timeout=60 * 60)
        return data


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        pk = self.kwargs['pk']
        key = f"category_{pk}"
        data = cache.get(key)
        if data:
            return data
        data = Category.objects.filter(pk=pk)
        cache.set(key, data, timeout=60 * 60)
        return data


class CategoryProductsAPIView(APIView):
    def get(self, request, pk):
        key = f"category_products_{pk}"
        data = cache.get(key)
        if data:
            return Response(data)

        products = Product.objects.filter(category_id=pk)
        serializer = ProductSerializer(products, many=True)
        cache.set(key, serializer.data, timeout=60 * 60)
        return Response(serializer.data)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCommentsAPIView(APIView):
    def get(self, request, pk):
        product = Product.objects.filter(pk=pk).first()
        if not product:
            return Response({"detail": "Product not found"}, status=404)
        comments = product.comments.all()
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)


class ProductImageListCreateAPIView(ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductImageDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductAttributeListCreateAPIView(ListCreateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductAttributeDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductPriceListCreateAPIView(ListCreateAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer


class ProductPriceDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer


class ProductCommentListCreateAPIView(ListCreateAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer


class ProductCommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer


class ProductRatingListCreateAPIView(ListCreateAPIView):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer


class ProductRatingDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            expires_in = int((datetime.datetime.fromtimestamp(access_token['exp']) - datetime.datetime.utcnow()).total_seconds())

            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
                'expires_in': expires_in,
                'expires_at': datetime.datetime.fromtimestamp(access_token['exp']).isoformat() + 'Z',
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
