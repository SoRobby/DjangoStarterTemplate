import inspect

from django.db import models
from django.template.defaultfilters import linebreaksbr
from django.utils.html import format_html


class FormFieldForDBFieldMixin:
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        field_type = db_field.get_internal_type()
        field.help_text = f'{field.help_text}<br>' \
                          f'Field name = "<code><small>{db_field.name}</small></code>"<br>' \
                          f'Field type = "<code><small>{field_type}</small></code>"'
        return field


class ModelDocumentationMixin:
    def list_model_methods(self, model_class):
        django_model_attributes = dir(models.Model)
        custom_exclusions = {'DoesNotExist', 'MultipleObjectsReturned', 'IntervalChoices'}
        custom_methods = set(dir(model_class)) - set(django_model_attributes) - custom_exclusions

        methods_with_docs = {
            meth: getattr(model_class, meth).__doc__ for meth in custom_methods
            if callable(getattr(model_class, meth))
               and not meth.startswith("__")
               and not meth.endswith("__")
               and inspect.getmodule(getattr(model_class, meth)) == inspect.getmodule(model_class)
        }

        sorted_methods_with_docs = sorted(methods_with_docs.items())
        return sorted_methods_with_docs

    def list_model_fields_and_properties(self, model_class):
        fields_and_props = [prop for prop in dir(model_class) if
                            not prop.startswith("__") and not callable(getattr(model_class, prop))]
        return fields_and_props

    def get_fieldsets(self, request, obj=None):
        # Use the class of the object if an instance is provided, otherwise use the model class of the admin
        model_class = obj.__class__ if obj else self.model
        fields_and_props_list_html = "<br>".join([f"- {field}" for field in self.list_model_fields_and_properties(model_class)])

        fields_and_props_description_html = format_html(f"""
            <b>Fields and properties:</b><br>
            {fields_and_props_list_html}<br>
        """)

        methods_with_docs_html = ""
        for method, doc in self.list_model_methods(model_class):
            docstring_html = linebreaksbr(doc) if doc else "No documentation available."
            methods_with_docs_html += f"<div style='margin-bottom:10px;'>" \
                                      f"<strong>{method}</strong><br>" \
                                      f"<div style='color:#4b5563;'>{docstring_html}</div>" \
                                      f"</div>"
        methods_with_docs_html = format_html(methods_with_docs_html)

        fields_and_props_fieldset = ('Model Fields/Properties', {
            'fields': (),
            'description': fields_and_props_description_html
        })
        methods_fieldset = ('Model Methods', {
            'fields': (),
            'description': methods_with_docs_html
        })

        # Ensure the base fieldsets are called from the correct super class
        base_fieldsets = super(ModelDocumentationMixin, self).get_fieldsets(request, obj)
        fieldsets = list(base_fieldsets) + [fields_and_props_fieldset, methods_fieldset]
        return fieldsets
