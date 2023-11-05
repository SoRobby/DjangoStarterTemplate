from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.db.models import Field
from django.db.models.fields.related import ForeignObjectRel

from apps.core.utils import AdminExportMixin, FormFieldForDBFieldMixin
from .models import SubscriptionPlan, SubscriptionTerm


# Register your models here.


# Register your models here.
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(FormFieldForDBFieldMixin, AdminExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'stripe_product_id', 'date_created', 'date_modified')

    list_filter = ('is_active',)

    filter_horizontal = ()

    search_fields = ()

    actions = ('export_as_csv', 'export_as_json', 'export_as_text')

    readonly_fields = ('id', 'uuid', 'date_created', 'date_modified')

    fieldsets = (
        ('Subscription plan information', {
            'fields': ('name', 'description', 'stripe_product_id', 'is_plan_showcased', 'features_list', 'json_data',
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


@admin.register(SubscriptionTerm)
class SubscriptionTermAdmin(FormFieldForDBFieldMixin, AdminExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'stripe_price_id', 'date_created', 'date_modified', 'list_model_attrs')

    list_filter = ('subscription_plan', 'interval', 'is_active')

    filter_horizontal = ()

    search_fields = ()

    actions = ('export_as_csv', 'export_as_json', 'export_as_text')

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

    # def list_model_attrs(self, obj=None):
    #     # Use dir() to list all attributes of the model including methods
    #     attrs = dir(SubscriptionTerm)
    #     # Optionally filter out private and magic methods
    #     attrs = [attr for attr in attrs if not attr.startswith('_')]
    #     return attrs

    # def list_model_attrs(self, obj=None):
    #     # Retrieve all attributes of the SubscriptionTerm class
    #     attrs = dir(SubscriptionTerm)
    #     # Retrieve all field names to exclude them from the list
    #     field_names = [field.name for field in SubscriptionTerm._meta.get_fields()]
    #     # Filter the attributes to get only custom methods and properties, excluding fields
    #     custom_attrs = [attr for attr in attrs if not attr.startswith('_') and attr not in field_names]
    #
    #     # Further filter to exclude anything that is not a method or property
    #     custom_methods_props = []
    #     for attr in custom_attrs:
    #         if isinstance(getattr(SubscriptionTerm, attr), property):
    #             custom_methods_props.append(attr)
    #         elif callable(getattr(SubscriptionTerm, attr)) and not isinstance(getattr(SubscriptionTerm, attr), Field):
    #             custom_methods_props.append(attr)
    #
    #     return custom_methods_props

    # def list_model_attrs(self, obj=None):
    #     # Retrieve all attributes of the SubscriptionTerm class
    #     custom_attrs = set(dir(SubscriptionTerm))
    #
    #     # Retrieve all field names to exclude them from the list
    #     field_names = set(field.name for field in SubscriptionTerm._meta.get_fields())
    #
    #     # Filter the attributes to exclude fields and Django model base attributes
    #     custom_methods_props = [attr for attr in custom_attrs if not attr.startswith('_') and attr not in field_names]
    #
    #     # Further filter to exclude anything that is not a method or property
    #     custom_only = []
    #     for attr in custom_methods_props:
    #         attribute = getattr(SubscriptionTerm, attr)
    #         if isinstance(attribute, property) or (callable(attribute) and not isinstance(attribute, type)):
    #             custom_only.append(attr)
    #
    #     return custom_only

    # def get_fieldsets(self, request, obj=None):
    #     # Create the description HTML for the custom fieldset
    #     attrs_description = self.list_model_attrs()
    #     attrs_list_html = "<br>".join([f"- {attr}" for attr in attrs_description])
    #     description_html = format_html(f"""
    #         <b>Model Attributes and Methods:</b><br>
    #         {attrs_list_html}<br>
    #     """)
    #
    #     # Custom fieldset to include model attributes and methods
    #     custom_fieldset = ('Model Attributes/Methods', {
    #         'fields': (),
    #         'description': description_html
    #     })
    #
    #     fieldsets = super().get_fieldsets(request, obj)
    #     fieldsets = list(fieldsets)  # Make sure we have a mutable version
    #     fieldsets.append(custom_fieldset)
    #     return fieldsets

    # VERSION 2
    # def list_model_attrs(self, obj=None):
    #     model = SubscriptionTerm  # Use the model class directly
    #     all_attrs = dir(model)
    #     fields_props = []
    #     methods_funcs = []
    #
    #     for attr in all_attrs:
    #         if not attr.startswith('_'):
    #             # Get the attribute
    #             attribute = getattr(model, attr)
    #             # Check if it's a field (but not a related object field)
    #             if isinstance(attribute, Field) and not isinstance(attribute, ForeignObjectRel):
    #                 fields_props.append(str(attr))
    #             # Check if it's a property
    #             elif isinstance(attribute, property):
    #                 fields_props.append(str(attr))
    #             # Check if it's a method
    #             elif callable(attribute) and not isinstance(attribute, (Field, property)):
    #                 methods_funcs.append(str(attr))
    #
    #     return fields_props, methods_funcs
    #
    #
    # def get_fieldsets(self, request, obj=None):
    #     fields_props, methods_funcs = self.list_model_attrs()
    #     print(fields_props)
    #     print(methods_funcs)
    #     fieldsets = super().get_fieldsets(request, obj)
    #     fieldsets += (
    #         ('Model Fields and Properties', {
    #             'description': 'These are the fields and properties of the model.'
    #         }),
    #     #     ('Model Methods and Functions', {
    #     #         'fields': methods_funcs,
    #     #         'description': 'These are the methods and functions of the model.'
    #     #     }),
    #     )
    #     return fieldsets


    # VERSION 3

