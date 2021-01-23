from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import Client, Comment
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
class CommentInline(admin.TabularInline):
    model = Comment


class ClientAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Client
    inlines = [
        CommentInline,
    ]
    actions = ["export_as_csv"]
    search_fields = ['author','name']

admin.site.register(Client, ClientAdmin)
admin.site.register(Comment)
