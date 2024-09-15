from hashlib import md5
from random import choice
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def generate_random_string():
    """
    Generates a random string consisting of 6 characters from the given letters.

    Returns:
        str: A random string consisting of 6 characters.
    """
    letters = "abcdef"
    random_string = ""
    for _ in range(6):
        random_string += choice(letters)
    return random_string


def generate_image_with_text(text):
    """
    Generates an image with the given text.

    Parameters:
        text (str): The text to be written on the image.

    Returns:
        str: The hash value of the image file.
    """

    # TODO: add a ratelimit for generation of 1 second
    image = Image.new("RGB", (70, 30), color=(255, 255, 255))

    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 5), text, font=font, fill=(0, 0, 0))

    current_date = datetime.now()
    iso_string = current_date.isoformat()
    binary_iso = bytes(iso_string, encoding="utf-8")
    hash = result = md5(binary_iso).hexdigest()

    image.save(f"img_{hash}.png")
    return hash
