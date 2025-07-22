from rest_framework import serializers
from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    image = serializers.ImageField(write_only=True, required=False, label='Upload photo')
    name = serializers.CharField(label='Enter title')
    description = serializers.CharField(label='Enter description')
    price = serializers.DecimalField(max_digits=10, decimal_places=2, label='Enter price')
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True, label='Enter category')
    is_active = serializers.BooleanField(label='Is Active?')
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id', 'is_active', 'created_at', 'updated_at', 'images', 'image']
        read_only_fields = ['id', 'created_at', 'updated_at', 'images', 'category']

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)
        if image:
            ProductImage.objects.create(product=product, image=image, is_main=True)
        return product
