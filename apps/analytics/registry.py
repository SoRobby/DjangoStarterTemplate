from django.apps import apps


class ViewRegistry:
    def __init__(self):
        self._registry = []

    def register(self, view_func=None, *, namespace, model, app=None, url_name=None):
        # Resolve model and app names from direct references or strings
        app_name = None
        model_name = None

        if isinstance(model, str):
            model_name = model
        else:
            model_name = model.__name__.lower()

        if app:
            if isinstance(app, str):
                app_name = app
            else:
                app_name = apps.get_app_config(app.__name__.lower()).name

        if view_func:
            app_name = app_name or view_func.__module__.split('.')[0]
            url_name = url_name or view_func.__name__

        self._registry.append({
            'app_name': app_name,
            'namespace': namespace,
            'model_name': model_name,
            'url_name': url_name
        })

        return view_func

    @property
    def registered_views(self):
        return self._registry


views_registry = ViewRegistry()


def register_view(namespace, model, app=None, url_name=None):
    def decorator(view_func):
        views_registry.register(view_func, namespace=namespace, model=model, app=app, url_name=url_name)
        return view_func

    return decorator

## Version 1.0
# class ViewRegistry:
#     def __init__(self):
#         self._registry = []
#
#     def register(self, view_func=None, *, namespace, model_name, app_name=None, url_name=None):
#         if view_func:  # if the decorator approach is used
#             app_name = app_name or view_func.__module__.split('.')[0]
#             url_name = url_name or view_func.__name__
#
#         self._registry.append({
#             'app_name': app_name,
#             'namespace': namespace,
#             'model_name': model_name,
#             'url_name': url_name
#         })
#
#         return view_func
#
#     @property
#     def registered_views(self):
#         return self._registry
#
#
# views_registry = ViewRegistry()
#
#
# def register_view(namespace, model_name, app_name=None, url_name=None):
#     def decorator(view_func):
#         views_registry.register(view_func, namespace=namespace, model_name=model_name, app_name=app_name,
#                                 url_name=url_name)
#         return view_func
#
#     return decorator
