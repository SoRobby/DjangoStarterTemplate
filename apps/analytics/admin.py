from django.contrib import admin

from .models import ObjectViewed


# Quick view register


# Register your models here.
@admin.register(ObjectViewed)
class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content_type', 'timestamp')

    list_filter = ()

    filter_horizontal = ()

    search_fields = ()

    readonly_fields = ('id', 'timestamp')

    fieldsets = (
        ('User properties', {
            'fields': (
                'user', 'ip_address'),
            'description': 'User related information'}
         ),

        ('Object information', {
            'fields': ('content_type', 'object_id'),
            'description': 'Object related information'}
         ),

        ('Read only properties', {
            'fields': ('id', 'timestamp'),
            'description': 'Ready only properties that cannot be modified'}
         ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        field_type = db_field.get_internal_type()
        field.help_text = f'{field.help_text}<br>' \
                          f'Field name = "<code><small>{db_field.name}</small></code>"<br>' \
                          f'Field type = "<code><small>{field_type}</small></code>"'
        return field
