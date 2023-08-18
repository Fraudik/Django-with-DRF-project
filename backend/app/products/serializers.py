from rest_framework import serializers
from rest_framework.reverse import reverse
from . import validators

from .models import Product
from users.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validators.unique_product_title])
    body = serializers.CharField(source='description')

    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='title'
    )

    owner = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'body',
            'price',
            'price_with_commission',

            'url',
            'edit_url',

            'owner',
        ]

    def get_product_user_data(self, obj) -> dict:
        return {
            "email": obj.user.email
        }

    def get_edit_url(self, obj) -> str:
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"title": obj.title}, request=request)
