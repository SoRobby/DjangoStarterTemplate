def str_to_bool(string_value):
    """
    Convert a string representation of a boolean value to a Python Boolean.

    Parameters:
    string_value (str): The string to convert.

    Returns:
    bool: The boolean value of the string.
    """
    return str(string_value).lower() in ('true', 'yes', 'on', '1')
