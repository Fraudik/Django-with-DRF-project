from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description') or title
        serializer.save(description=description)


class ProductDetailAPIView(generics.RetrieveAPIView):
    lookup_field = "title"
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


product_create_view = ProductCreateAPIView.as_view()
product_detail_view = ProductDetailAPIView.as_view()
