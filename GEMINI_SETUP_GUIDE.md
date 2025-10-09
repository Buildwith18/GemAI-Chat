# Google Generative AI Setup Guide

## ✅ Available Models

The `gemini-1.5-flash` model has been deprecated. Current available models include:

- `gemini-1.5-flash-001` (specific version - **RECOMMENDED**)
- `gemini-1.5-pro-001` (more capable but slower)
- `gemini-1.5-flash-latest` (alias to latest stable)
- `gemini-2.0-flash-exp` (experimental)

## ✅ Recommended Replacement Model

**Use `gemini-1.5-flash-001`** instead of `gemini-1.5-flash`. This is the most stable and widely available option.

## ✅ Corrected Python Example

### Using google.generativeai SDK (Fixed):

```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use the correct model name
model = genai.GenerativeModel("gemini-1.5-flash-001")

# Generate content
response = model.generate_content("What is AI?")
print(response.text)
```

### Using REST API (More Reliable):

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_BASE = "https://generativelanguage.googleapis.com/v1beta"

def generate_content(prompt: str, model_name: str = "gemini-1.5-flash-001"):
    url = f"{GOOGLE_BASE}/models/{model_name}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 512,
            "temperature": 0.7
        }
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

# Usage
result = generate_content("What is AI?")
print(result)
```

## ✅ Steps to Verify Setup

### 1. Get Google AI API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Create a new API key
4. Copy the key (starts with `AIza...`)

### 2. Set Environment Variables

Create a `.env` file in your project root:

```bash
GOOGLE_API_KEY=your_api_key_here
FALLBACK_MODEL=gemini-1.5-flash-001
```

### 3. Test Your Setup

Run the verification script:

```bash
python verify_gemini_setup.py
```

Or use the Django management command:

```bash
cd backend
python manage.py test_gemini --test-generation
```

### 4. Verify API Key Permissions

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to "APIs & Services" > "Credentials"
3. Find your API key
4. Ensure it has access to "Generative Language API"

### 5. Check Model Availability

The verification script will show you:

- ✅ Available models for your API key
- ✅ Models supporting `generateContent`
- ✅ Recommended model to use
- ✅ Test generation with the recommended model

## ✅ Your Django Backend is Already Fixed!

Your Django backend (`backend/chatbot/views.py`) already includes:

1. **✅ Automatic model discovery** - Lists available models on startup
2. **✅ Smart model selection** - Chooses the best available model
3. **✅ Fallback mechanism** - Uses `FALLBACK_MODEL` if auto-discovery fails
4. **✅ Proper error handling** - Handles HTTP errors and model unavailability
5. **✅ REST API implementation** - More reliable than SDK

## ✅ Quick Fix for Your Current Issue

Simply update your `.env` file:

```bash
# Add this to your .env file
FALLBACK_MODEL=gemini-1.5-flash-001
```

Then restart your Django server:

```bash
cd backend
python manage.py runserver
```

## ✅ Testing Your Setup

1. **Test the health endpoint:**

   ```bash
   curl http://localhost:8000/health/
   ```

2. **Test chat functionality:**
   ```bash
   curl -X POST http://localhost:8000/chatbot/reply/ \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello, how are you?", "user_id": "test", "session_id": "test"}'
   ```

## ✅ Troubleshooting

### If you still get 404 errors:

1. **Check your API key:**

   ```bash
   python verify_gemini_setup.py
   ```

2. **Check Django logs:**

   ```bash
   cd backend
   python manage.py test_gemini --test-generation
   ```

3. **Verify model availability:**
   - The startup logs will show which model was selected
   - Check the health endpoint response for `selected_model`

### Common Issues:

- **API Key not set**: Make sure `GOOGLE_API_KEY` is in your `.env` file
- **Wrong model name**: Use `gemini-1.5-flash-001` instead of `gemini-1.5-flash`
- **API permissions**: Ensure your API key has access to Generative Language API
- **Rate limits**: Check if you've exceeded API quotas

## ✅ Production Recommendations

1. **Use specific model versions** (e.g., `gemini-1.5-flash-001`) instead of aliases
2. **Implement retry logic** for temporary failures
3. **Monitor API usage** and set up billing alerts
4. **Use environment-specific API keys** for different deployments
5. **Implement caching** for frequently asked questions

Your Django backend is already well-architected with automatic model discovery and fallback mechanisms!
