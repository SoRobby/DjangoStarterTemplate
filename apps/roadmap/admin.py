from django.contrib import admin

from .models import Category, Feature

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name')

    list_filter = ()

    filter_horizontal = ()

    search_fields = ('name',)

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified')

    prepopulated_fields = {'slug': ('name',), }

    fieldsets = (
        ('Category', {
            'fields': (
                'name', 'slug', 'description'),
            'description': 'Primary category fields'}
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



@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'release_status', 'date_created', 'date_modified')

    list_filter = ('release_status',)

    filter_horizontal = ()

    search_fields = ('name',)

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified', 'date_archived', 'date_released')

    fieldsets = (
        ('Feature', {
            'fields': (
                'name', 'description', 'category', 'up_votes'),
            'description': 'Primary post fields and content'}
         ),

        ('Status information', {
            'fields': ('release_status', 'date_released', 'date_archived'),
            'description': 'Information about feature creation, modification, and deletion'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_created', 'date_modified'),
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
                ''',}
         ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        field_type = db_field.get_internal_type()
        field.help_text = f'{field.help_text}<br>' \
                          f'Field name = "<code><small>{db_field.name}</small></code>"<br>' \
                          f'Field type = "<code><small>{field_type}</small></code>"'
        return field