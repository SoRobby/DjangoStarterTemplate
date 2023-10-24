from django.contrib import admin

from .models import UserSession, ObjectViewed


# Register your models here.
@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_session_active', 'date_created', 'date_modified')

    list_filter = ('is_session_active', )

    filter_horizontal = ()

    search_fields = ()

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified', 'date_session_ended', 'expire_date')

    fieldsets = (
        ('Session and user information', {
            'fields': ('session_key', 'user', 'is_session_active', 'session_data_onload', 'session_data_beforeunload'),
            'description': 'Object related information'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_created', 'date_modified', 'date_session_ended', 'expire_date'),
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


@admin.register(ObjectViewed)
class ObjectViewedAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content_type', 'user_session', 'date_viewed')

    list_filter = ()

    filter_horizontal = ()

    search_fields = ()

    readonly_fields = ('id', 'uuid', 'date_viewed')

    fieldsets = (
        ('Object information', {
            'fields': ('content_type', 'object_id'),
            'description': 'Object related information'}
         ),

        ('User and session properties', {
            'fields': (
                'user', 'user_session', 'ip_address'),
            'description': 'User related information'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_viewed'),
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
