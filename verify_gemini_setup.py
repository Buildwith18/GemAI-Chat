#!/usr/bin/env python3
"""
Google Generative AI Setup Verification Script
This script helps verify your Google AI API setup and test model availability.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_BASE = "https://generativelanguage.googleapis.com/v1beta"

def check_api_key():
    """Check if API key is properly configured."""
    print("🔑 Checking API Key Configuration...")
    
    if not API_KEY:
        print("❌ GOOGLE_API_KEY not found in environment variables")
        print("   Please set GOOGLE_API_KEY in your .env file")
        return False
    
    if len(API_KEY) < 20:
        print("❌ API key appears to be too short (should be ~39 characters)")
        return False
    
    print(f"✅ API key found: {API_KEY[:10]}...{API_KEY[-4:]}")
    return True

def list_available_models():
    """List all available models for the API key."""
    print("\n📋 Listing Available Models...")
    
    url = f"{GOOGLE_BASE}/models?key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        models = data.get("models", [])
        
        if not models:
            print("❌ No models found in API response")
            return []
        
        print(f"✅ Found {len(models)} models:")
        
        generate_content_models = []
        for model in models:
            name = model.get("name", "Unknown")
            methods = model.get("supportedGenerationMethods", [])
            supports_generate = "generateContent" in methods
            
            status = "✅" if supports_generate else "❌"
            print(f"   {status} {name}")
            print(f"      Methods: {', '.join(methods)}")
            
            if supports_generate:
                generate_content_models.append(name)
        
        return generate_content_models
        
    except requests.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response:
            print(f"   Response: {e.response.text}")
        return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_model_generation(model_name):
    """Test generating content with a specific model."""
    print(f"\n🧪 Testing Model: {model_name}")
    
    # Clean model name
    clean_name = model_name.replace("models/", "")
    url = f"{GOOGLE_BASE}/models/{clean_name}:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Hello! Please respond with 'Test successful' if you can read this."}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 50,
            "temperature": 0.1
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract text from response
        text = extract_text_from_response(data)
        print(f"✅ Model {model_name} working!")
        print(f"   Response: {text[:100]}...")
        return True
        
    except requests.HTTPError as e:
        print(f"❌ HTTP Error with {model_name}: {e}")
        if e.response:
            print(f"   Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Error with {model_name}: {e}")
        return False

def extract_text_from_response(response_json):
    """Extract text from Google AI response."""
    try:
        candidates = response_json.get("candidates", [])
        if candidates:
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if parts:
                return parts[0].get("text", "")
        return str(response_json)
    except:
        return str(response_json)

def recommend_model(models):
    """Recommend the best model to use."""
    print("\n💡 Model Recommendations:")
    
    if not models:
        print("❌ No suitable models found")
        return None
    
    # Scoring system
    candidates = []
    for model in models:
        name = model.lower()
        score = 0
        
        if "gemini" in name:
            score += 5
        if "flash" in name:
            score += 3
        if "pro" in name:
            score += 2
        if "001" in name:
            score += 2
        if "latest" in name:
            score += 1
        if any(x in name for x in ("exp", "experimental", "beta")):
            score -= 5
            
        candidates.append((score, model))
    
    candidates.sort(reverse=True, key=lambda x: x[0])
    recommended = candidates[0][1]
    
    print(f"✅ Recommended: {recommended}")
    print(f"   Score: {candidates[0][0]}")
    
    if len(candidates) > 1:
        print("\n   Alternative options:")
        for score, model in candidates[1:3]:
            print(f"   - {model} (score: {score})")
    
    return recommended

def main():
    """Main verification function."""
    print("🚀 Google Generative AI Setup Verification")
    print("=" * 50)
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    # List models
    models = list_available_models()
    if not models:
        print("\n❌ No models supporting generateContent found")
        sys.exit(1)
    
    # Recommend model
    recommended = recommend_model(models)
    
    # Test recommended model
    if recommended:
        success = test_model_generation(recommended)
        if success:
            print(f"\n🎉 Setup verification complete!")
            print(f"✅ Use this model in your code: {recommended}")
            print(f"\n📝 Add to your .env file:")
            print(f"FALLBACK_MODEL={recommended}")
        else:
            print(f"\n❌ Recommended model failed testing")
            sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Verification complete! Your setup should work now.")

if __name__ == "__main__":
    main()
