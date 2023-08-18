from rest_framework import mixins, viewsets
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from users.mixins import StaffPermissionMixin
from ..models import Product
from ..serializers import ProductSerializer


@extend_schema_view(
    update=extend_schema(
        summary="Update product info by title.",
        responses={
            403: OpenApiResponse(description='Forbidden.'),
            404: OpenApiResponse(description="Product with such title not found.")
        },
    ),
    destroy=extend_schema(
        summary="Delete product by title.",
        responses={
            403: OpenApiResponse(description='Forbidden.'),
            404: OpenApiResponse(description="Product with such title not found.")
        },
    )
)
class ProductViewSet(
    StaffPermissionMixin,

    viewsets.ModelViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'title'


@extend_schema_view(
    retrieve=extend_schema(
        summary="Get product by title.",
        responses={
            404: OpenApiResponse(description="Product with such title not found.")
        },
    ),
)
class ProductGenericViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'title'
