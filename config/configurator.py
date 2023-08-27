import logging
import re

from django.conf import settings
from django.template import base as template_base

# Check if the configuration setting for multiline template tags is enabled
if settings.MULTILINE_TEMPLATE_TAGS:
    # If enabled, update the regular expression pattern used by the template engine
    # The template engine seems to have a variable called `template_base` representing the base template
    # `tag_re` is a regular expression pattern used to identify tags within the template
    # The `re.compile()` function compiles a regular expression pattern into a regular expression object
    # The `pattern` attribute of `template_base.tag_re` holds the original pattern
    # The `re.DOTALL` flag is used to make the `.` character match any character, including newline characters

    # The code block updates the regular expression pattern used by a template engine
    # if the configuration setting MULTILINE_TEMPLATE_TAGS is enabled. It enables the
    # engine to recognize and process multiline tags correctly by adding the re.DOTALL
    # flag to the pattern.

    template_base.tag_re = re.compile(template_base.tag_re.pattern, re.DOTALL)
    logging.debug('[CORE.BASE_TEMPLATE_SETUP] Multiline template tags enabled')
