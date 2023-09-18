from django.contrib import admin

from .models import Country


# Register your models here.
@admin.register(Country)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'country_code')

    list_filter = ()

    filter_horizontal = ()

    search_fields = ('name', 'country_code')

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified')

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Country', {
            'fields': ('name', 'slug', 'country_code', 'phone_code'),
            'description': 'Information about the country'}
         ),
        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_created', 'date_modified'),
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
