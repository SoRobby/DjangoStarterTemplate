import types

from django.db import models


class ViewsRegistry:
    registered_views = []

    @classmethod
    def register(cls, namespace, url_name, app_name, model):
        if isinstance(model, str):
            model_name = model
        elif issubclass(model, models.Model):
            model_name = model.__name__.lower()
        else:
            raise TypeError("model_name_or_class should either be a string or a Django Model class.")

        cls.registered_views.append({
            'namespace': namespace,
            'url_name': url_name,
            'app_name': app_name,
            'model_name': model_name,
        })


views_registry = ViewsRegistry()


# views_registry.register(namespace="blog", url_name="post", app_name="blog", model_name="post")


def register_view(namespace, url_name, app_name, model):
    def decorator(obj):
        # Register the view
        views_registry.register(namespace, url_name, app_name, model)

        # If it's a function (FBV), return it as is
        if isinstance(obj, types.FunctionType):
            return obj

        # If it's a class (CBV), hook into its dispatch method
        elif isinstance(obj, type):  # It's a class
            original_dispatch = obj.dispatch

            def new_dispatch(*args, **kwargs):
                return original_dispatch(*args, **kwargs)

            obj.dispatch = new_dispatch
            return obj

        else:
            raise TypeError("Unsupported type for the decorator")

    return decorator

