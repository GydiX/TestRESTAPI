from django.shortcuts import render
from rest_framework import viewsets
from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        resp = requests.get(GOOGLE_USERINFO_URL, headers={"Authorization": f"Bearer {code}"})
        if resp.status_code != 200:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        userinfo = resp.json()
        return Response(userinfo)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category').prefetch_related('images')
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        headers = self.get_success_headers(serializer.data)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED, headers=headers)

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all().select_related('product')
    serializer_class = ProductImageSerializer
    filterset_fields = ['product', 'is_main']