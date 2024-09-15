from utils import generate_random_string, generate_image_with_text
from pathlib import Path
from os import environ as env, getenv
from flask import Flask, Response, request, jsonify, send_file

db = {}
app = Flask(__name__)


@app.route("/")
def homepage():
    return "Texthuman - Checking humans by images and text"


@app.route("/generate")
# Will return the hash of the image, which will then be used to validate the text of the captcha.
def generate():
    """
    Generates a random string, generates an image with the generated text,
    stores the text in the database with the image hash as the key,
    and returns the image hash as a response.

    Returns:
        Response: The image hash as a response.
    """
    text = generate_random_string()
    image_hash = generate_image_with_text(text)
    db[image_hash] = text
    return Response(image_hash, mimetype="text/plain")


@app.route("/image")
def get_image_by_hash():
    """
    Get an image by its hash. Returns the image with the specified hash if it exists, otherwise returns an error message.
    
    Parameters:
        None
         
    Returns:
        If the hash is not specified, returns a JSON response with an error message indicating that no hash was specified.
        If the image with the specified hash does not exist, returns a JSON response with an error message indicating that no image was found with the specified hash.
        If the image with the specified hash exists, returns the image file.
        
    Raises:
        None
    """
    hash = request.args.get("id")
    if hash is None:
        return (
            jsonify(
                {
                    "error": "No hash specified",
                    "description": "Please specify a hash that has been returned when the image was generated.",
                }
            ),
            400,
        )

    image = Path(f'{getenv("PWD")}/img_{hash}.png')
    if not image.exists():
        # The captcha with the specified hash does not exist
        return (
            jsonify(
                {
                    "error": "No test with the hash found",
                    "description": "A test was not found with the specified hash. The hash might be invalid, check the specified hash.",
                }
            ),
            404,
        )

    # The captcha exists
    return send_file(image, mimetype="image/png")


@app.route("/validate")
def validate_captcha():
    """
    Validates a captcha by comparing the provided hash and text with the stored values in the database.

    Returns:
        A JSON response indicating whether the captcha is valid or not.

    Raises:
        None
    """
    hash = request.args.get("id")
    text = request.args.get("text")
    if hash is None:
        return (
            jsonify(
                {
                    "error": "No hash specified",
                    "description": "Please specify a hash that has been returned when the image was generated.",
                }
            ),
            400,
        )
    if text is None:
        return (
            jsonify(
                {
                    "error": "No text specified",
                    "description": "Please specify the text to validate.",
                }
            ),
            400,
        )

    if db[hash] == text:
        return jsonify({"valid": True, "text": text})

    return jsonify({"valid": False, "text": text})


if __name__ == "__main__":
    if "API_PORT" in env:
        port = getenv("API_PORT")
    else:
        port = 3000
    app.run(debug=True, port=port)
