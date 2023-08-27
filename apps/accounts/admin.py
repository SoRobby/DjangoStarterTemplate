# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import Account


# Admin objects
@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_admin', 'is_superuser', 'date_joined')

    list_filter = ('email_verified', 'is_admin', 'is_staff')

    filter_horizontal = ()

    search_fields = ('email', 'username')

    readonly_fields = ('id', 'uuid', 'short_uuid', 'email_verification_token', 'last_login', 'date_joined')

    fieldsets = (
        ('General information', {
            'fields': ('email', 'username', 'name'),
            'description': 'General account information'}
         ),

        ('User preferences', {
            'fields': ('profile_image', 'description', 'theme', 'is_profile_public'),
            'description': 'General account information'}
         ),

        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser'),
            'description': 'Permissions for the account'}
         ),

        ('Email verification', {
            'fields': ('email_verified', 'email_verification_token'),
            'description': 'Account verification parameters'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'short_uuid', 'last_login', 'date_joined'),
            'description': 'Ready only properties that cannot be modified'}
         ),

        ('Notes', {
            'fields': (),
            'description': '''
                <b>Additional properties:</b><br>
                - full_name: Returns the full name of the user (first_name + last_name)<br>
            '''}
         ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
         ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        field_type = db_field.get_internal_type()
        print(f'field = {field}')
        field.help_text = f'{field.help_text}<br>' \
                          f'Field name = "<code><small>{db_field.name}</small></code>"<br>' \
                          f'Field type = "<code><small>{field_type}</small></code>"'
        return field
