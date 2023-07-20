from rest_framework import serializers
from rest_framework.reverse import reverse
from . import validators

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validators.unique_product_title])
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
            view_name='product-detail',
            lookup_field='title'
    )

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'price_with_commission',

            'url',
            'edit_url',
        ]

    def get_edit_url(self, obj):
        request = self.context.get('request') # self.request
        if request is None:
            return None
        return reverse("product-edit", kwargs={"title": obj.title}, request=request)
