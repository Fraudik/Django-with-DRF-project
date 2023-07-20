from rest_framework import generics, mixins, permissions, authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Product
from .serializers import ProductSerializer


class ProductMixinView(
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
    # authentication_classes = [JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        requested_title = kwargs.get("title")
        if requested_title is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description') or title
        serializer.save(description=description)


product_mixin_view = ProductMixinView.as_view()
