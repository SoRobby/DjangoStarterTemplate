from django.contrib import admin

from apps.blog.models import Post, Comment


# Blog objects

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'release_status', 'date_created', 'date_modified', 'date_published')

    list_filter = ('release_status',)

    filter_horizontal = ()

    search_fields = ('title',)

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified', 'date_deleted')

    fieldsets = (
        ('Post', {
            'fields': (
                'title', 'slug', 'lead_author', 'release_status', 'content', 'content2', 'featured_image',
                'featured_image_thumbnail', 'featured_image_raw', 'date_published'),
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'is_flagged', 'is_deleted', 'date_created', 'date_modified')

    list_filter = ('is_deleted',)

    filter_horizontal = ('upvotes', 'downvotes')

    search_fields = ('content',)

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified', 'date_deleted')

    fieldsets = (
        ('Comment', {
            'fields': (
                'post', 'parent_comment', 'user', 'content'),
            'description': 'Primary comment fields and content'}
         ),

        ('Social properties', {
            'fields': ('upvotes', 'downvotes'),
            'description': 'Post vote information'}
         ),

        ('Audit information', {
            'fields': ('is_edited', 'is_flagged', 'is_deleted'),
            'description': 'Audit information about the comment'}
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
