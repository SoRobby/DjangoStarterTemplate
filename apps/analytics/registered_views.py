from apps.blog.models import Post
from .registry import views_registry

# Registered views to track
# views_registry.register(
#     app_name='blog',
#     namespace='blog',
#     model_name='post',
#     url_name='post',
# )

views_registry.register(
    app='blog',
    model=Post,
    namespace='blog',
    url_name='post',
)

# views_registry.register(
#     app_name='product',
#     namespace='products',
#     model_name='product',
#     url_name='product',
# )
