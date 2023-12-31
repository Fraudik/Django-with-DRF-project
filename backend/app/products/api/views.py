from rest_framework import generics, mixins
from drf_spectacular.utils import extend_schema, OpenApiResponse
from users.mixins import StaffPermissionMixin, UserQuerySetMixin
from ..models import Product
from ..serializers import ProductSerializer


class ProductMixinView(
    UserQuerySetMixin,
    StaffPermissionMixin,

    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'title'

    @extend_schema(
        responses={
            403: OpenApiResponse(description='Forbidden.'),
            404: OpenApiResponse(description="Product with such title not found.")
        }
    )
    def get(self, request, *args, **kwargs):
        requested_title = kwargs.get("title")
        if requested_title is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    @extend_schema(
        responses={
            403: OpenApiResponse(description='Forbidden.'),
            404: OpenApiResponse(description="Product with such title not found.")
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description') or title
        serializer.save(description=description)
