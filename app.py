import os
import base64
import logging
from io import BytesIO
from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBomlqfYty6yX-232HCGPx5EqhbDfXFOB8")
genai.configure(api_key=API_KEY)

# Set the model
MODEL_NAME = "gemini-2.0-flash"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok"})

@app.route('/extract-gemini', methods=['POST'])
def extract_prescription():
    """
    Extract text from prescription image using Gemini.

    Accepts:
    - image: A prescription image file
    - prompt: Optional prompt text (default: "read the prescription")

    Returns:
    - JSON with extracted text or error message
    """
    try:
        # Check if image file is present in request
        if 'image' not in request.files:
            return jsonify({"success": False, "error": "No image file provided"}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"success": False, "error": "Empty image file provided"}), 400

        # Get prompt from request or use default
        prompt = request.form.get('prompt', 'read the prescription')

        # Process the image
        img = Image.open(image_file)

        # Convert image to bytes for Gemini API
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=img.format or 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Initialize Gemini model
        model = genai.GenerativeModel(MODEL_NAME)

        # Create content parts for the model
        image_parts = [
            {
                "mime_type": f"image/{img.format.lower() if img.format else 'jpeg'}",
                "data": base64.b64encode(img_byte_arr).decode('utf-8')
            }
        ]

        # Generate content with the model
        response = model.generate_content([prompt, image_parts[0]])

        # Extract and return the result
        result = response.text
        return jsonify({"success": True, "result": result})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
