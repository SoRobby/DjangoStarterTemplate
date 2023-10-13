# VIEWS_TO_TRACK = [
#     {
#         'namespace': 'blog',
#         'url_name': 'post',
#         'app_name': 'blog',
#         'model_name': 'post'
#     },
#     # Add other views you want to track as needed.
# ]


class ViewRegistry:
    def __init__(self):
        self._registry = []

    def register(self, **kwargs):
        self._registry.append(kwargs)

    @property
    def registered_views(self):
        return self._registry


views_registry = ViewRegistry()


views_registry.register(
    app_name='blog',
    namespace='blog',
    model_name='post',
    url_name='post',
)

views_registry.register(
    app_name='product',
    namespace='products',
    model_name='product',
    url_name='product',
)
