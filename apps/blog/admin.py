from django.contrib import admin

from apps.blog.models import Post


# Blog objects

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'release_status', 'date_created', 'date_modified', 'date_published')

    list_filter = ('release_status',)

    filter_horizontal = ('authors',)

    search_fields = ('title',)

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified', 'date_deleted')

    fieldsets = (
        ('Post', {
            'fields': ('title', 'slug', 'lead_author', 'authors', 'release_status', 'content', 'featured_image', 'date_published'),
            'description': 'Primary post fields and content'}
         ),

        ('SEO and meta properties', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'description': 'SEO meta tags'}
         ),

        ('Settings', {
            'fields': ('allow_comments', 'allow_sharing'),
            'description': 'Post settings and permissions'}
         ),

        ('Audit information', {
            'fields': ('created_by', 'modified_by', 'deleted_by', 'is_deleted'),
            'description': 'Information about post creation, modification, and deletion'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_created', 'date_modified', 'date_deleted'),
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

#
# @admin.register(Account)
# class AccountAdmin(UserAdmin):
#     list_display = ('email', 'username', 'is_staff', 'is_admin', 'is_superuser', 'date_joined')
#
#     list_filter = ('is_admin', 'is_staff')
#
#     filter_horizontal = ()
#
#     search_fields = ('email', 'username')
#
#     readonly_fields = ('id', 'uuid', 'short_uuid', 'email_verification_token', 'last_login', 'date_joined')
#
#     fieldsets = (
#         ('General information', {
#             'fields': ('email', 'username', 'name'),
#             'description': 'General account information'}
#          ),
#
#         ('User Preferences', {
#             'fields': ('profile_image', 'description', 'theme', 'is_profile_public'),
#             'description': 'General account information'}
#          ),
#
#         ('Permissions', {
#             'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser'),
#             'description': 'Permissions for the account'}
#          ),
#
#         ('Email verification', {
#             'fields': ('email_verified', 'email_verification_token'),
#             'description': 'Account verification parameters'}
#          ),
#
#         ('Read only properties', {
#             'fields': ('id', 'uuid', 'short_uuid', 'last_login', 'date_joined'),
#             'description': 'Ready only properties that cannot be modified'}
#          ),
#
#         ('Notes', {
#             'fields': (),
#             'description': '''
#                 <b>Additional properties:</b><br>
#                 - full_name: Returns the full name of the user (first_name + last_name)<br>
#             '''}
#          ),
#     )
#
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'password1', 'password2')}
#          ),
#     )
