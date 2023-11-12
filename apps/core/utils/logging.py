import inspect
import logging


def log_view_call():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])

    if "self" in frame.frame.f_locals:
        cls = frame.frame.f_locals["self"].__class__
        caller_name = f"{cls.__name__}.{frame.function}"
    else:
        caller_name = frame.function

    module_name = module.__name__.split('.')[-2] if module else 'unknown'
    logging.debug(f'[{module_name.upper()}.{caller_name.upper()}] Called')
