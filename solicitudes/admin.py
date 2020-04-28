from django.contrib import admin

from .models import Solicitud
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class SolicitudResource(resources.ModelResource):
    class Meta:
        model = Solicitud


class SolicitudAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'domicilio', 'colonia', 'telefono', 'entrega')
    search_fields = ['domicilio']
    resource_class = SolicitudResource


admin.site.register(Solicitud, SolicitudAdmin)
