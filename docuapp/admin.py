# admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Office, Expedient, ReceiveExpedient, DocType
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin, GroupAdmin as DefaultGroupAdmin
from .resources import GroupResource, UserResource


admin.site.site_header = "Sistema de Trámite Documentario | TRAMITEC"
admin.site.site_title = "TRAMITEC"

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ImportExportModelAdmin, DefaultUserAdmin):
    resource_class = UserResource
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin, DefaultGroupAdmin):
    resource_class = GroupResource
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DocType)
class DocTypeAdmin(ImportExportModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',)  

@admin.register(Office)
class OfficeAdmin(ImportExportModelAdmin):
    list_display = ('name', 'user', 'created_at') 
    search_fields = ('name',)  
    filter_horizontal = ('groups',)  

@admin.register(Expedient)
class ExpedientAdmin(admin.ModelAdmin):
    list_display = ('code', 'document', 'doc_number', 'destination', 'folio', 'condition', 'user', 'created_at')  
    readonly_fields = ('created_at',)

@admin.register(ReceiveExpedient)
class ReceiveExpedientAdmin(admin.ModelAdmin):
    list_display = ('expedient', 'destination', 'condition', 'destination', 'date_attention', 'user', 'created_at') 
    readonly_fields = ('created_at',)
