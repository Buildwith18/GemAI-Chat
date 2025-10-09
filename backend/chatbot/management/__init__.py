"""
Django management command to test Google Generative AI integration
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class Command(BaseCommand):
    help = 'Test Google Generative AI integration and model availability'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-generation',
            action='store_true',
            help='Test actual content generation',
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Specific model to test',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Testing Google Generative AI Integration'))
        
        # Check API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.stdout.write(self.style.ERROR('❌ GOOGLE_API_KEY not found in environment'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ API Key found: {api_key[:10]}...{api_key[-4:]}'))
        
        # List models
        models = self.list_models(api_key)
        if not models:
            self.stdout.write(self.style.ERROR('❌ No models found'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'✅ Found {len(models)} models'))
        
        # Show models supporting generateContent
        generate_models = []
        for model in models:
            name = model.get("name", "Unknown")
            methods = model.get("supportedGenerationMethods", [])
            if "generateContent" in methods:
                generate_models.append(name)
                self.stdout.write(f'  ✅ {name}')
            else:
                self.stdout.write(f'  ❌ {name} (no generateContent)')
        
        if not generate_models:
            self.stdout.write(self.style.ERROR('❌ No models support generateContent'))
            return
        
        # Test specific model or recommend one
        if options['model']:
            test_model = options['model']
        else:
            test_model = self.recommend_model(generate_models)
        
        self.stdout.write(self.style.SUCCESS(f'🎯 Testing model: {test_model}'))
        
        # Test generation if requested
        if options['test_generation']:
            success = self.test_generation(test_model, api_key)
            if success:
                self.stdout.write(self.style.SUCCESS('🎉 Content generation test passed!'))
            else:
                self.stdout.write(self.style.ERROR('❌ Content generation test failed'))
        else:
            self.stdout.write('💡 Use --test-generation to test actual content generation')
        
        # Show configuration recommendations
        self.stdout.write('\n📝 Configuration Recommendations:')
        self.stdout.write(f'FALLBACK_MODEL={test_model}')
        self.stdout.write(f'GOOGLE_API_KEY={api_key[:10]}...{api_key[-4:]}')

    def list_models(self, api_key):
        """List available models"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data.get("models", [])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error listing models: {e}'))
            return []

    def recommend_model(self, models):
        """Recommend the best model"""
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
        return candidates[0][1]

    def test_generation(self, model_name, api_key):
        """Test content generation"""
        clean_name = model_name.replace("models/", "")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_name}:generateContent?key={api_key}"
        
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
            
            # Extract text
            text = self.extract_text(data)
            self.stdout.write(f'📝 Response: {text}')
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Generation error: {e}'))
            return False

    def extract_text(self, response_json):
        """Extract text from response"""
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
