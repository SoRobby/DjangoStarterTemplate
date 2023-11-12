from io import BytesIO

from PIL import Image
from django.core.files import File


def process_image(image, crop_dimensions=None, resize_dimensions=None, file_format=None):
    """
    Process an image by cropping and resizing it. Optionally set the file format.

    Parameters:
    - image (PIL.Image): The original image.
    - crop_dimensions (tuple, optional): The x, y, width, and height to crop the image. Default is None.
    - resize_dimensions (tuple, optional): The new width and height to resize the image. Default is None.
    - file_format (str, optional): The desired file format ('png', 'jpeg', etc.). Default is None.

    Returns:
    - django.core.files.File: Processed image file.
    """

    # If resize_dimensions is provided, perform cropping and resizing
    if resize_dimensions:
        # Extract x, y, width, and height from crop_dimensions
        x, y, width, height = crop_dimensions

        # Crop the image based on provided dimensions
        image = image.crop((x, y, x + width, y + height))

        # Resize the image based on provided dimensions
        image = image.resize(resize_dimensions, Image.LANCZOS)

    # If no file_format is provided, use the format of the original image
    if file_format is None:
        file_format = image.format

    # Convert PIL image to BytesIO
    image_io = BytesIO()

    # Save the PIL image in BytesIO object, using the provided or original format
    image.save(image_io, format=file_format)

    # Return the BytesIO object as a Django File object
    return File(image_io)
