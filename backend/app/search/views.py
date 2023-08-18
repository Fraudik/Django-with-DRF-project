from rest_framework import generics
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from products.models import Product
from products.serializers import ProductSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='title', description='Title of product', type=str),
        ]
    )
)
class SearchListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        query_search = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('title')
        results = Product.objects.none()
        if query is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = query_search.search(query, user=user)
        return results
