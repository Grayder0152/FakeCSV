from django.contrib import admin

from .models import Schema, Column, DataSet

admin.site.register(Column)
admin.site.register(DataSet)


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ('title', 'modified', 'column_separator', 'string_separator', 'user_id')