from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from .permissions import UserProfilesPermissions
from ..serializers import UserSerializer


@extend_schema_view(
    retrieve=extend_schema(
        summary="Fetch user profile by `id`.",
        responses={
            200: OpenApiResponse(response=UserSerializer,
                                 description="User profile fetched successfully."),
            403: OpenApiResponse(description='Forbidden.'),
            404: OpenApiResponse(description="User with such 'id' not found.")
        },
    ),
    destroy=extend_schema(
        summary="Delete user account by `id`.",
        responses={
            204: OpenApiResponse(response=UserSerializer,
                                 description="User account deleted successfully."),
            403: OpenApiResponse(description='Forbidden.'),
            404: OpenApiResponse(description="User with such 'id' not found.")
        },
    )
)
class UserFetchDeleteViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin
):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserProfilesPermissions]
