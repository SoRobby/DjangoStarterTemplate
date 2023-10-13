from .views_registry import views_registry

# Registered views
views_registry.register(namespace="blog", url_name="post", app_name="blog", model_name="post")
