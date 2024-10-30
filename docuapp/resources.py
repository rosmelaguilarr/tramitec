# resources.py
from import_export import resources
from django.contrib.auth.models import Group, User
from .models import Office
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget

class GroupResource(resources.ModelResource):
    class Meta:
        model = Group
        fields = ('id', 'name')
        export_order = ('id', 'name')


class UserResource(resources.ModelResource):
    groups = fields.Field(
        column_name='groups',
        attribute='groups',
        widget=ManyToManyWidget(Group, separator=',', field='name')
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 
            'email', 'is_active', 'groups'
        )
        export_order = (
            'id', 'username', 'first_name', 'last_name', 
            'email', 'is_active', 'groups'
        )

class OfficeResource(resources.ModelResource):
    groups = fields.Field(
        column_name='groups',
        attribute='groups',
        widget=ManyToManyWidget(Group, separator=',', field='name')
    )

    class Meta:
        model = Office
        fields = ('id', 'name', 'user', 'groups', 'created_at')