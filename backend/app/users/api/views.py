from rest_framework import status, generics, mixins
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth import get_user_model, authenticate, login, password_validation
from django.contrib.auth.hashers import make_password
from django.db.models.query import prefetch_related_objects
from django.shortcuts import get_object_or_404
from django.conf import settings
from .permissions import UserProfilesUpdatePermissions
from ..models import CustomUser
from ..serializers import UserAuthSerializer, UserRegisterSerializer, UserLoginSerializer, UserSerializer, OTPSerializer
from ..tasks import send_otp_email


class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    @extend_schema(
        summary="Register user",
        responses={
            201: OpenApiResponse(response=UserSerializer,
                                 description='User registered successfully.'),
            400: OpenApiResponse(description='Bad request.'),
            403: OpenApiResponse(description='Incorrect CSRF token.'),
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.get('password')
        password_validation.validate_password(password)
        serializer.validated_data['password'] = make_password(password)

        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User registered successfully",
        },
            status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @extend_schema(
        summary="Login user",
        responses={
            201: OpenApiResponse(response=UserSerializer,
                                 description='OTP sent.'),
            400: OpenApiResponse(description='Bad request.'),
            401: OpenApiResponse(description='Invalid credentials.'),
            403: OpenApiResponse(description='Incorrect CSRF token.'),
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = authenticate(request,
                            email=data['email'],
                            password=data['password'])
        if user is not None:
            # Generate and update OTP
            user.confirmation_otp = settings.TOTP_GENERATOR.now()
            user.save()
            # Send OTP
            send_otp_email.delay(user.email, user.confirmation_otp)

            return Response(data="OTP sent",
                            status=status.HTTP_201_CREATED)
        return Response(data="Invalid credentials",
                        status=status.HTTP_401_UNAUTHORIZED)


class UserConfirmOTPView(generics.GenericAPIView):
    serializer_class = OTPSerializer

    @extend_schema(
        summary="Verify OTP for login",
        responses={
            200: OpenApiResponse(response=UserSerializer,
                                 description='OTP verified successfully.'),
            400: OpenApiResponse(description='Bad request.'),
            401: OpenApiResponse(description='OTP expired.'),
            403: OpenApiResponse(description='Incorrect CSRF token.'),
            404: OpenApiResponse(description='No user with such OTP.'),
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.data['otp']
        if not settings.TOTP_GENERATOR.verify(otp):
            return Response(data="OTP expired",
                            status=status.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(CustomUser, confirmation_otp=otp)
        login(request, user)
        user.confirmation_otp = None
        user.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User logged in successfully",
        })


class UserUpdateView(
    generics.GenericAPIView,
    mixins.UpdateModelMixin,
):
    """ Separate view for update to allow changing password """
    queryset = get_user_model().objects.all()
    serializer_class = UserAuthSerializer
    lookup_field = "id"
    # Allow only owner to update his profile
    permission_classes = [UserProfilesUpdatePermissions]

    def update(self, request, *args, **kwargs):
        """ Rewrite update function to add password hashing """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        changed_password = serializer.validated_data.get('password')
        if changed_password is not None:
            password_validation.validate_password(changed_password)
            serializer.validated_data['password'] = make_password(changed_password)
        self.perform_update(serializer)

        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance,
            # and then re-prefetch related objects
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)

        returned_data = serializer.data
        # Return password only if it has been changed, in plain form
        if changed_password is not None:
            returned_data["password"] = changed_password
        else:
            del returned_data["password"]
        return Response(returned_data)

    @extend_schema(
        summary="Update user profile by `id`.",
        responses={
            200: OpenApiResponse(response=UserSerializer,
                                 description="User profile updated successfully."),
            400: OpenApiResponse(description='Bad request.'),
            403: OpenApiResponse(description='Forbidden.'),
            404: OpenApiResponse(description="User with such 'id' not found.")
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
