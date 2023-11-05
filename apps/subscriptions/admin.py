from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.template.defaultfilters import linebreaksbr

import inspect
from apps.core.utils import AdminExportMixin, FormFieldForDBFieldMixin, ModelDocumentationMixin
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
class SubscriptionTermAdmin(ModelDocumentationMixin, FormFieldForDBFieldMixin, AdminExportMixin, admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'stripe_price_id', 'date_created', 'date_modified')

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

    # def list_model_methods(self):
    #     # Retrieve all methods, excluding dunder methods
    #     methods = [func for func in dir(SubscriptionTerm) if callable(getattr(SubscriptionTerm, func)) and not func.startswith("__")]
    #     return methods

    # def list_model_methods(self):
    #     # Get the methods from the Django Model base class to exclude them
    #     django_model_methods = {func for func in dir(models.Model) if callable(getattr(models.Model, func))}
    #
    #     # Retrieve all methods from your model, excluding the ones from Django Model
    #     custom_methods = set(dir(SubscriptionTerm)) - django_model_methods
    #
    #     # Exclude any remaining dunder methods and sort the list
    #     custom_methods = sorted([meth for meth in custom_methods if
    #                              not meth.startswith("__") and callable(getattr(SubscriptionTerm, meth))])
    #
    #     return custom_methods


    # def list_model_methods(self):
    #     # Get all attributes from the Django Model base class to exclude them
    #     django_model_attributes = dir(models.Model)
    #
    #     # Define any custom exclusions from your model
    #     custom_exclusions = {
    #         'DoesNotExist',
    #         'MultipleObjectsReturned',
    #         'IntervalChoices',
    #         # Add any additional attributes that you want to exclude
    #     }
    #
    #     # Retrieve all attributes from your model, excluding the ones from Django Model
    #     # and any custom exclusions you've defined
    #     custom_methods = set(dir(SubscriptionTerm)) - set(django_model_attributes) - custom_exclusions
    #
    #     # Filter to include only methods, exclude magic methods and sort the list
    #     custom_methods = sorted([
    #         meth for meth in custom_methods
    #         if callable(getattr(SubscriptionTerm, meth))
    #         and not meth.startswith("__")
    #         and not meth.endswith("__")
    #         # Additional check for excluding methods not defined directly in the model class
    #         and inspect.getmodule(getattr(SubscriptionTerm, meth)) == inspect.getmodule(SubscriptionTerm)
    #     ])
    #
    #     return custom_methods





    # def get_fieldsets(self, request, obj=None):
    #     # Fields and properties description
    #     fields_and_props_list_html = "<br>".join([f"- {field}" for field in self.list_model_fields_and_properties()])
    #     fields_and_props_description_html = format_html(f"""
    #         <b>Model Fields and Properties:</b><br>
    #         {fields_and_props_list_html}<br>
    #     """)
    #
    #     # Methods description
    #     methods_list_html = "<br>".join([f"- {method}" for method in self.list_model_methods()])
    #     methods_description_html = format_html(f"""
    #         <b>Model Methods:</b><br>
    #         {methods_list_html}<br>
    #     """)
    #
    #     # Custom fieldsets
    #     fields_and_props_fieldset = ('Model Fields/Properties', {
    #         'fields': (),
    #         'description': fields_and_props_description_html
    #     })
    #
    #     methods_fieldset = ('Model Methods', {
    #         'fields': (),
    #         'description': methods_description_html
    #     })
    #
    #     fieldsets = super().get_fieldsets(request, obj)
    #     fieldsets = list(fieldsets)  # Make sure we have a mutable version
    #     fieldsets.append(fields_and_props_fieldset)
    #     fieldsets.append(methods_fieldset)
    #     return fieldsets

    # def list_model_methods(self):
    #     # Get all attributes from the Django Model base class to exclude them
    #     django_model_attributes = dir(models.Model)
    #
    #     # Define any custom exclusions from your model
    #     custom_exclusions = {
    #         'DoesNotExist',
    #         'MultipleObjectsReturned',
    #         'IntervalChoices',
    #         # Add any additional attributes that you want to exclude
    #     }
    #
    #     # Retrieve all attributes from your model, excluding the ones from Django Model
    #     # and any custom exclusions you've defined
    #     custom_methods = set(dir(SubscriptionTerm)) - set(django_model_attributes) - custom_exclusions
    #
    #     # Construct a dictionary of method names to their docstrings
    #     methods_with_docs = {
    #         meth: getattr(SubscriptionTerm, meth).__doc__ for meth in custom_methods
    #         if callable(getattr(SubscriptionTerm, meth))
    #         and not meth.startswith("__")
    #         and not meth.endswith("__")
    #         and inspect.getmodule(getattr(SubscriptionTerm, meth)) == inspect.getmodule(SubscriptionTerm)
    #     }
    #
    #     # Sort the methods by name
    #     sorted_methods_with_docs = sorted(methods_with_docs.items())
    #
    #     print(sorted_methods_with_docs)
    #
    #     return sorted_methods_with_docs
    #
    #
    # def list_model_fields_and_properties(self):
    #     # Retrieve all fields and properties, excluding dunder properties and methods
    #     fields_and_props = [prop for prop in dir(SubscriptionTerm) if
    #                         not prop.startswith("__") and not callable(getattr(SubscriptionTerm, prop))]
    #     return fields_and_props
    #
    #
    # def get_fieldsets(self, request, obj=None):
    #     # Fields and properties description
    #     fields_and_props_list_html = "<br>".join([f"- {field}" for field in self.list_model_fields_and_properties()])
    #     fields_and_props_description_html = format_html(f"""
    #         <b>Fields and properties:</b><br>
    #         {fields_and_props_list_html}<br>
    #     """)
    #
    #     # Methods description with docstrings
    #     # methods_with_docs_html = format_html("<b>Model Methods:</b><br>") + format_html("".join(
    #     #     [format_html("<div style='margin-bottom:10px;'>"
    #     #                  "<strong>{}</strong>"
    #     #                  "<div style='color:#666;'>{}</div>"
    #     #                  "</div>", method, linebreaksbr(doc)) for method, doc in self.list_model_methods()]
    #     # ))
    #
    #     methods_with_docs_html = ""
    #     for method, doc in self.list_model_methods():
    #         docstring_html = linebreaksbr(doc) if doc else "No documentation available."
    #         methods_with_docs_html += f"<div style='border: 1px solid #e5e7eb; border-radius: 0.25rem; padding: 0.5rem;'>" \
    #                                   f"<strong>{method}</strong>" \
    #                                   f"<div style='color:#4b5563;'>{docstring_html}</div>" \
    #                                   f"</div>"
    #
    #     # Format the entire HTML string
    #     methods_with_docs_html = format_html(methods_with_docs_html)
    #
    #     # Custom fieldsets
    #     fields_and_props_fieldset = ('Model Fields/Properties', {
    #         'fields': (),
    #         'description': fields_and_props_description_html
    #     })
    #
    #     methods_fieldset = ('Model Methods', {
    #         'fields': (),
    #         'description': methods_with_docs_html
    #     })
    #
    #     fieldsets = super().get_fieldsets(request, obj)
    #     fieldsets = list(fieldsets)  # Make sure we have a mutable version
    #     fieldsets.append(fields_and_props_fieldset)
    #     fieldsets.append(methods_fieldset)
    #     return fieldsets
