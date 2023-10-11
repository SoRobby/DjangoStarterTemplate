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


class ColorizeFilter(logging.Filter):
    """
    A custom logging filter that applies different ANSI color codes to messages
    based on their logging level.

    Attributes:
        COLORS (dict): A mapping of log level names to their respective ANSI color codes.
        RESET (str): ANSI escape code to reset the color to terminal's default.
    """

    # Define a dictionary mapping logging level names to ANSI color codes
    COLORS = {
        "DEBUG": "\033[96m",        # Cyan
        "INFO": "\033[94m",         # Blue
        "WARNING": "\033[93m",      # Yellow
        "ERROR": "\033[91m",        # Light red
        "CRITICAL": "\033[31m",     # Dark red
    }

    # ANSI escape code to reset the color to terminal's default
    RESET = "\033[0m"

    def filter(self, record):
        """
        Modify the record's message to prepend it with an ANSI color code based
        on the record's levelname. If the levelname is not found in the COLORS
        dictionary, the RESET color is used as a default.

        Args:
            record (logging.LogRecord): The log record to be processed.

        Returns:
            bool: True always, allowing the log message to be processed by
                  further filters/handlers.
        """
        levelname = record.levelname
        record.msg = f"{self.COLORS.get(levelname, self.RESET)}{record.msg}{self.RESET}"
        return True
