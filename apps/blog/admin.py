from django.contrib import admin

from apps.blog.models import Article, Comment
from apps.core.utils import AdminExportMixin, ModelDocumentationMixin


# Blog objects

@admin.register(Article)
class ArticleAdmin(ModelDocumentationMixin, AdminExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'release_status', 'date_created', 'date_modified', 'date_published')

    list_filter = ('release_status', 'visibility', 'is_deleted')

    filter_horizontal = ()

    search_fields = ('title',)

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified', 'date_deleted')

    fieldsets = (
        ('Post', {
            'fields': (
                'title', 'slug', 'lead_author', 'release_status', 'visibility', 'content', 'featured_image',
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
                    - published: Returns all article's that have the status of "published"<br>
                    - in_review: Returns all article's that have the status of "review"<br>
                    - in_draft: Returns all article's that have the status of "draft"<br>
                    - not_published: Returns all article's that have not been published<br>
                    <b>Deleting logic:</b><br>
                    - On deletion: When an instance is deleted, all of the instance data (featured images and images in the rich text editor will be deleted)<br>
                '''}
         ),
    )


@admin.register(Comment)
class CommentAdmin(ModelDocumentationMixin, AdminExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'user', 'is_flagged', 'is_deleted', 'date_created', 'date_modified')

    list_filter = ('is_flagged', 'is_deleted')

    filter_horizontal = ('likes', 'dislikes')

    search_fields = ('content',)

    autocomplete_fields = ('article', 'user')

    actions = ('uncheck_is_flagged', 'export_as_csv', 'export_as_json', 'export_as_text')

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified', 'date_deleted')

    fieldsets = (
        ('Comment', {
            'fields': (
                'article', 'user', 'parent_comment', 'content'),
            'description': 'Primary comment fields and content'}
         ),

        ('Social properties', {
            'fields': ('likes', 'dislikes'),
            'description': 'Article user like and dislike information'}
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

    def get_queryset(self, request):
        # Use the 'admin_objects' manager to get the queryset for the admin view
        qs = self.model.admin_objects.get_queryset()

        # If you need to apply any admin-specific filtering or ordering, you can do so here
        # For example, if you want to order by 'date_created' you can do:
        # qs = qs.order_by('-date_created')

        return qs

    def uncheck_is_flagged(self, request, queryset):
        queryset.update(is_flagged=False)

