from rest_framework.routers import DefaultRouter

from products.api.viewsets import ProductGenericViewSet

router = DefaultRouter()
router.register('products', ProductGenericViewSet, basename='products')
urlpatterns = router.urls
