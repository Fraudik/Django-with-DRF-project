import decimal
from django.db import models
from django.conf import settings
from django.db.models import Q

from users.models import CustomUser


class ProductQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(description__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#primary-key (commentary below)
    # Django will automatically add a field to hold the primary key
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#unique (commentary below)
    # Note that when unique is True, you don’t need to specify db_index, because unique implies the creation of an index
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, unique=True, null=False)
    # https://docs.djangoproject.com/en/dev/ref/models/fields/#null (commentary below)
    # Avoid using null on string-based fields such as CharField and TextField.
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    @property
    def price_with_commission(self) -> float:
        return round(self.price * decimal.Decimal(1 + settings.GLOBAL_SETTINGS['COMMISSION_VALUE']), 2)
