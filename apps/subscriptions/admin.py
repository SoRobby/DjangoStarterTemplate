from django.contrib import admin

from apps.core.utils import AdminExportMixin, ModelDocumentationMixin
from .models import SubscriptionPlan, SubscriptionPeriod, SubscriptionOrder

# Register your models here.

admin.site.register(SubscriptionOrder)


# Register your models here.
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelDocumentationMixin, AdminExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'plan_category', 'is_active', 'stripe_product_id', 'date_created')

    list_filter = ('plan_category', 'is_active',)

    filter_horizontal = ()

    search_fields = ('name', 'description')

    actions = ('export_as_csv', 'export_as_json', 'export_as_text')

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified')

    fieldsets = (
        ('Subscription plan information', {
            'fields': (
            'name', 'plan_category', 'description', 'stripe_product_id', 'is_plan_showcased', 'features_list',
            'json_data',
            'is_active'),
            'description': 'Object related information'}
         ),

        ('Admin information', {
            'fields': ('admin_notes',),
            'description': 'Object related information'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_created', 'date_modified'),
            'description': 'Ready only properties that cannot be modified'}
         ),
    )


@admin.register(SubscriptionPeriod)
class SubscriptionPeriodAdmin(ModelDocumentationMixin, AdminExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'stripe_price_id', 'date_created')

    list_filter = ('subscription_plan', 'interval', 'is_active')

    filter_horizontal = ()

    search_fields = ()

    autocomplete_fields = ('subscription_plan',)

    actions = ('set_selected_active', 'export_as_csv', 'export_as_json', 'export_as_text')

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified')

    fieldsets = (
        ('Subscription term information', {
            'fields': ('subscription_plan', 'interval', 'stripe_price_id', 'price_cents', 'is_active'),
            'description': 'Object related information'}
         ),

        ('Admin information', {
            'fields': ('admin_notes',),
            'description': 'Object related information'}
         ),

        ('Read only properties', {
            'fields': ('id', 'uuid', 'date_created', 'date_modified'),
            'description': 'Ready only properties that cannot be modified'}
         ),
    )

    def set_selected_active(self, request, queryset):
        queryset.update(is_active=True)
