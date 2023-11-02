from django.core.files.storage import default_storage


def save_file_to_field(model_instance, field_name, file, directory_path, file_name=None):
    """
    Save a file to a specific field on a model instance, replacing the old file if it exists.

    Parameters:
    - model_instance: Django model instance where the file will be saved.
    - field_name (str): The name of the field where the file will be saved.
    - file (File): The file to save.
    - directory_path (str): The directory where the file should be saved.
    - file_name (str, optional): The name to save the file as. If None, uses the existing filename.
    """
    if file_name is None:
        file_name = file.name

    # Create the full path for the file
    file_path = f"{directory_path}/{file_name}"

    # Delete the old file if it exists
    old_file_path = getattr(model_instance, field_name).path if getattr(model_instance, field_name) else None
    if old_file_path and default_storage.exists(old_file_path):
        default_storage.delete(old_file_path)

    # Save the new file
    default_storage.save(file_path, file)

    # Update the model field with the new file path
    setattr(model_instance, field_name, file_path)
    model_instance.save()
