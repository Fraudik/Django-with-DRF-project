from rest_framework.validators import UniqueValidator
from .models import Product

unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')
