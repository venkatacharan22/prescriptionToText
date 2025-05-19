# GeminiRxExtractor

A Flask backend that uses Google's Gemini model to extract text from prescription images.

## Features

- Exposes a `/extract-gemini` POST endpoint that accepts prescription images
- Uses Google's Gemini 2.0 Flash model for image analysis
- Provides a `/health` endpoint for health checks
- Configurable via environment variables

## Setup

### Prerequisites

- Python 3.8+
- Google Gemini API key

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd GeminiRxExtractor
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your API key:

   Create a `.env` file in the project root with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

   Or set it as an environment variable:
   ```
   export GOOGLE_API_KEY=your_api_key_here
   ```

### Running Locally

Start the server:
```
python app.py
```

The server will run on `http://localhost:5001` by default.

## API Usage

### Health Check

```
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

### Extract Text from Prescription

```
POST /extract-gemini
```

Parameters (multipart/form-data):
- `image`: The prescription image file (required)
- `prompt`: Custom prompt for the Gemini model (optional, default: "read the prescription")

Example using curl:
```bash
curl -X POST http://localhost:5001/extract-gemini \
  -F "image=@path/to/prescription.jpg" \
  -F "prompt=extract all medication details from this prescription"
```

Successful Response:
```json
{
  "success": true,
  "result": "Extracted text from the prescription..."
}
```

Error Response:
```json
{
  "success": false,
  "error": "Error message..."
}
```

## Using with Postman

1. Create a new POST request to `http://localhost:5001/extract-gemini`
2. In the "Body" tab, select "form-data"
3. Add a key "image" with type "File" and select your image file
4. Optionally add a key "prompt" with type "Text" and enter your custom prompt
5. Send the request

## Docker Deployment

Build the Docker image:
```
docker build -t gemini-rx-extractor .
```

Run the container:
```
docker run -p 8080:8080 -e GOOGLE_API_KEY=your_api_key_here gemini-rx-extractor
```

The server will be available at `http://localhost:8080`.

## Deploying to Render

This repository is configured for easy deployment to [Render](https://render.com/).

### Automatic Deployment

1. Fork or clone this repository to your GitHub account
2. Sign up for a Render account if you don't have one
3. In Render dashboard, click "New" and select "Blueprint"
4. Connect your GitHub account and select this repository
5. Render will automatically detect the `render.yaml` configuration
6. Add your `GOOGLE_API_KEY` as an environment variable
7. Click "Apply" to deploy the service

### Manual Deployment

1. Sign up for a Render account if you don't have one
2. In Render dashboard, click "New" and select "Web Service"
3. Connect your GitHub repository
4. Use the following settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add the environment variable:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
6. Click "Create Web Service"

Your API will be available at the URL provided by Render (e.g., `https://gemini-rx-extractor.onrender.com`).

## Notes

- For production use, always use a secure API key management solution
- The fallback API key in the code is for development purposes only
- When deploying to Render, make sure to set the `GOOGLE_API_KEY` environment variable
