# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import Account, AccountSettings


# Admin objects
@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_admin', 'is_superuser', 'date_joined')

    list_filter = ('email_verified', 'is_admin', 'is_staff', 'is_marked_for_deletion')

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

        ('Account deletion', {
            'fields': ('is_marked_for_deletion', 'date_marked_for_deletion'),
            'description': 'Account deletion parameters'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'short_uuid', 'date_joined', 'last_login'),
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
        field.help_text = f'{field.help_text}<br>' \
                          f'Field name = "<code><small>{db_field.name}</small></code>"<br>' \
                          f'Field type = "<code><small>{field_type}</small></code>"'
        return field


@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'account', 'date_created', 'date_modified')

    list_filter = ()

    filter_horizontal = ()

    search_fields = ()

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified')

    fieldsets = (
        ('Account', {
            'fields': ('account',),
            'description': 'Primary comment fields and content'}
         ),

        ('Privacy settings', {
            'fields': ('show_email',),
            'description': 'Privacy related settings for the account'}
         ),

        ('Email settings', {
            'fields': ('marketing_emails', 'weekly_digest_emails', 'discovery_emails', 'site_update_emails'),
            'description': 'Type of emails the user will receive'}
         ),

        ('Notification settings', {
            'fields': ('inbox_message_notifications', 'announcement_notifications'),
            'description': 'Type of notifications the user will receive'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_created', 'date_modified'),
            'description': 'Ready only properties that cannot be modified'}
         ),

        ('Notes', {
            'fields': (),
            'description': '''
                    <b>Query manager:</b><br>
                    - published: Returns all Post's that have the status of "published"<br>
                    - in_review: Returns all Post's that have the status of "review"<br>
                    - in_draft: Returns all Post's that have the status of "draft"<br>
                '''}
         ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        field_type = db_field.get_internal_type()
        field.help_text = f'{field.help_text}<br>' \
                          f'Field name = "<code><small>{db_field.name}</small></code>"<br>' \
                          f'Field type = "<code><small>{field_type}</small></code>"'
        return field
