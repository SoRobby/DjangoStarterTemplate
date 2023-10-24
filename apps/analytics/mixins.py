from .signals import object_viewed_signal


class ObjectViewMixin(object):
    # TODO - May want to fix this: https://youtu.be/SMRaHSZiwWE?t=1688
    # Mixin is only applicable to class based views.
    def get_context_data(self, *args, **kwargs):
        context = super(ObjectViewMixin, self).get_context_data(*args, **kwargs)
        instance = context.get('object')
        if instance:
            object_viewed_signal.send(instance.__class__, instance=instance, request=self.request)
        return context


    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         instance = self.get_object()
    #     except DoesNotExist:
    #         instance = None
    #     if instance is not None:
    #         object_viewed_signal.send(instance.__class__, instance=instance, request=request)
    #     return super(ObjectViewMixin, self).dispatch(request, *args, **kwargs)
