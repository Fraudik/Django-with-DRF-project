import decimal
from django.db import models
from django.conf import settings

from users.models import User


class Product(models.Model):
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#primary-key (commentary below)
    # Django will automatically add a field to hold the primary key
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#unique (commentary below)
    # Note that when unique is True, you don’t need to specify db_index, because unique implies the creation of an index
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, unique=True, null=False)
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#null (commentary below)
    # Avoid using null on string-based fields such as CharField and TextField.
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    @property
    def price_with_commission(self):
        return round(self.price * decimal.Decimal(1 + settings.GLOBAL_SETTINGS['COMMISSION_VALUE']), 2)
