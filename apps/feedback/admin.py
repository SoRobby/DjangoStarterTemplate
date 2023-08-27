from django.contrib import admin

from apps.feedback.models import Feedback


# Register your models here.
@admin.register(Feedback)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'page_url', 'is_processed', 'date_created', 'date_modified')

    list_filter = ('category', 'is_processed')

    filter_horizontal = ()

    search_fields = ('category', 'page_url', 'content')

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified')

    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'user'),
            'description': 'Information about the user that submitted the feedback'}
         ),

        ('Feedback', {
            'fields': ('page_url', 'category', 'content'),
            'description': 'Primary post fields and content'}
         ),

        ('Processing', {
            'fields': ('is_processed',),
            'description': 'Has the feedback been processed?'}
         ),

        ('Read Only Properties', {
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