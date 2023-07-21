import copy
from rest_framework import permissions


class IsStaff(permissions.DjangoModelPermissions):

    # https://stackoverflow.com/questions/46584653/django-rest-framework-use-djangomodelpermissions-on-listapiview
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
