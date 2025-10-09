# # from django.http import JsonResponse

# # def chatbot_reply(request):
# #     return JsonResponse({"message": "Hello from chatbot!"})

# #chatbot/views.py
# # chatbot/views.py
# # chatbot/views.py

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.db import connection
# from django.db.utils import OperationalError
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import json
# from .models import ChatMessage, ChatSession
# from django.utils import timezone

# # Load environment variables
# load_dotenv()

# # Configure Gemini
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# def check_database_connection():
#     """Check if database is connected and accessible"""
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT 1")
#             return True, "Database connection successful"
#     except OperationalError as e:
#         return False, f"Database connection failed: {str(e)}"
#     except Exception as e:
#         return False, f"Unexpected database error: {str(e)}"

# @csrf_exempt
# def health_check(request):
#     """Health check endpoint to verify database connectivity"""
#     if request.method == 'GET':
#         db_connected, db_message = check_database_connection()
        
#         response_data = {
#             "status": "healthy" if db_connected else "unhealthy",
#             "database": {
#                 "connected": db_connected,
#                 "message": db_message
#             },
#             "timestamp": timezone.now().isoformat()
#         }
        
#         status_code = 200 if db_connected else 503
#         return JsonResponse(response_data, status=status_code)

# @csrf_exempt
# def chatbot_reply(request):
#     if request.method == 'POST':
#         try:
#             # Check database connection first
#             db_connected, db_message = check_database_connection()
#             if not db_connected:
#                 print(f"Database connection failed: {db_message}")
#                 return JsonResponse({"error": "Database connection failed"}, status=503)
            
#             data = json.loads(request.body)
#             prompt = data.get("prompt", "")
#             user_id = data.get("user_id", "anonymous")
#             session_id = data.get("session_id", "default")
            
#             print("Received prompt:", prompt)
#             print("User ID:", user_id)
#             print("Session ID:", session_id)

#             if not prompt:
#                 return JsonResponse({"error": "Prompt is required."}, status=400)

#             # Save user message to database
#             try:
#                 user_message = ChatMessage.objects.create(
#                     user_id=user_id,
#                     text=prompt,
#                     sender='user',
#                     session_id=session_id
#                 )
#                 print(f"Saved user message to database: {user_message.id}")
#             except Exception as e:
#                 print(f"Failed to save user message: {e}")
#                 # Continue with API call even if DB save fails

#             # Create a more structured prompt for better responses
#             structured_prompt = f"""
# You are an AI tutor helping a student learn. Please provide a clear, structured response to the following question:

# Question: {prompt}

# Please format your response with:
# 1. A clear, concise answer
# 2. If there are steps, number them clearly (1., 2., 3., etc.)
# 3. If there are multiple options, list them with bullet points (•)
# 4. Use **bold** for important terms and concepts
# 5. Use proper line breaks (\n) to separate paragraphs
# 6. Keep responses helpful but concise
# 7. Use clear formatting for lists and steps

# Format your response with proper line breaks and structure. For example:
# - Use double line breaks (\n\n) between sections
# - Use single line breaks (\n) for list items
# - Bold important terms with **term**
# - Number steps clearly: 1. First step, 2. Second step, etc.

# Response:
# """

#             response = model.generate_content(structured_prompt)
#             print("Gemini full response:", response)

#             # Safely extract reply text
#             if hasattr(response, 'text'):
#                 reply = response.text
#             elif hasattr(response, 'parts'):
#                 reply = ''.join([part.text for part in response.parts])
#             else:
#                 reply = str(response)

#             # Save AI response to database
#             try:
#                 ai_message = ChatMessage.objects.create(
#                     user_id=user_id,
#                     text=reply,
#                     sender='ai',
#                     session_id=session_id
#                 )
#                 print(f"Saved AI response to database: {ai_message.id}")
#             except Exception as e:
#                 print(f"Failed to save AI response: {e}")

#             return JsonResponse({"reply": reply})
#         except Exception as e:
#             print(f"Error in chatbot_reply: {e}")
#             return JsonResponse({"error": str(e)}, status=500)

#     return JsonResponse({"message": "Send a POST request with a prompt."})

# @csrf_exempt
# def get_chat_history(request):
#     """Get chat history for a user"""
#     if request.method == 'GET':
#         try:
#             user_id = request.GET.get('user_id', 'anonymous')
#             session_id = request.GET.get('session_id', 'default')
            
#             # Check database connection
#             db_connected, db_message = check_database_connection()
#             if not db_connected:
#                 return JsonResponse({"error": "Database connection failed"}, status=503)
            
#             messages = ChatMessage.objects.filter(
#                 user_id=user_id,
#                 session_id=session_id
#             ).order_by('timestamp')
            
#             chat_history = []
#             for msg in messages:
#                 chat_history.append({
#                     'id': str(msg.id),
#                     'text': msg.text,
#                     'sender': msg.sender,
#                     'timestamp': msg.timestamp.isoformat()
#                 })
            
#             return JsonResponse({
#                 "messages": chat_history,
#                 "count": len(chat_history)
#             })
#         except Exception as e:
#             print(f"Error getting chat history: {e}")
#             return JsonResponse({"error": str(e)}, status=500)
    
#     return JsonResponse({"error": "GET method required"}, status=405)

# @csrf_exempt
# def clear_chat(request):
#     """Clear chat messages for a specific user and session"""
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_id = data.get('user_id', 'anonymous')
#             session_id = data.get('session_id', 'default')
            
#             # Check database connection
#             db_connected, db_message = check_database_connection()
#             if not db_connected:
#                 return JsonResponse({"error": "Database connection failed"}, status=503)
            
#             # Delete messages for this user and session
#             deleted_count = ChatMessage.objects.filter(
#                 user_id=user_id, 
#                 session_id=session_id
#             ).delete()[0]
            
#             print(f"Cleared {deleted_count} messages for user {user_id}, session {session_id}")
            
#             return JsonResponse({
#                 "status": "success",
#                 "deleted_count": deleted_count,
#                 "message": f"Cleared {deleted_count} messages"
#             })
#         except Exception as e:
#             print(f"Error clearing chat: {e}")
#             return JsonResponse({"error": str(e)}, status=500)
    
#     return JsonResponse({"error": "POST method required"}, status=405)

# @csrf_exempt
# def get_sessions(request):
#     """Get all chat sessions for a user"""
#     if request.method == 'GET':
#         try:
#             user_id = request.GET.get('user_id', 'anonymous')
            
#             # Check database connection
#             db_connected, db_message = check_database_connection()
#             if not db_connected:
#                 return JsonResponse({"error": "Database connection failed"}, status=503)
            
#             # Get unique sessions for this user
#             sessions = ChatMessage.objects.filter(
#                 user_id=user_id
#             ).values('session_id').distinct().order_by('-timestamp')
            
#             session_list = []
#             for session in sessions:
#                 session_id = session['session_id']
#                 # Get the first message timestamp for this session
#                 first_message = ChatMessage.objects.filter(
#                     user_id=user_id,
#                     session_id=session_id
#                 ).order_by('timestamp').first()
                
#                 if first_message:
#                     session_list.append({
#                         'session_id': session_id,
#                         'created_at': first_message.timestamp.isoformat(),
#                         'message_count': ChatMessage.objects.filter(
#                             user_id=user_id,
#                             session_id=session_id
#                         ).count()
#                     })
            
#             return JsonResponse({
#                 "sessions": session_list,
#                 "count": len(session_list)
#             })
#         except Exception as e:
#             print(f"Error getting sessions: {e}")
#             return JsonResponse({"error": str(e)}, status=500)
    
#     return JsonResponse({"error": "GET method required"}, status=405)



# chatbot/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.db.utils import OperationalError
from dotenv import load_dotenv
import os
import json
import requests
import logging
from .models import ChatMessage, ChatSession
from django.utils import timezone

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
GOOGLE_BASE = "https://generativelanguage.googleapis.com/v1beta"
API_KEY = os.getenv("GOOGLE_API_KEY")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "")  # e.g. "gemini-2.5-flash"

if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in your environment (.env) before running.")

# Globals populated at import/startup
SELECTED_MODEL_ID = None
AVAILABLE_MODELS = []

def check_database_connection():
    """Check if database is connected and accessible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return True, "Database connection successful"
    except OperationalError as e:
        return False, f"Database connection failed: {str(e)}"
    except Exception as e:
        return False, f"Unexpected database error: {str(e)}"

def list_models(api_key: str):
    """Call ListModels and return models list (or empty)."""
    url = f"{GOOGLE_BASE}/models?key={api_key}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("models", [])

def choose_model(models: list):
    """
    Improved model selection with better heuristics:
      - prefer models containing 'gemini'
      - prefer ones that list 'generateContent' in supported methods
      - prefer 'flash'/'pro' and specific versions (001, latest)
      - avoid experimental models unless no other option
    Returns model identifier (string) or None.
    """
    candidates = []
    for m in models:
        name = m.get("name") or m.get("model") or m.get("modelId") or ""
        if not name:
            continue
            
        nm_lower = name.lower()
        methods = m.get("supportedGenerationMethods") or m.get("supportedMethods") or m.get("supported_methods") or []
        if isinstance(methods, list):
            methods_text = " ".join(methods).lower()
        else:
            methods_text = str(methods).lower()
            
        supports_generate = "generatecontent" in methods_text
        is_gemini = "gemini" in nm_lower
        is_experimental = any(x in nm_lower for x in ("exp", "experimental", "beta"))
        
        # Scoring system
        score = 0
        if supports_generate:
            score += 10
        if is_gemini:
            score += 5
        if "flash" in nm_lower:
            score += 3
        if "pro" in nm_lower:
            score += 2
        if "001" in nm_lower:  # Prefer specific versions
            score += 2
        if "latest" in nm_lower:  # Prefer latest aliases
            score += 1
        if is_experimental:
            score -= 5  # Penalize experimental models
            
        candidates.append((score, name, supports_generate, is_experimental))
    
    if not candidates:
        return None
        
    # Sort by score (descending), prefer non-experimental
    candidates.sort(reverse=True, key=lambda t: (t[0], not t[3]))
    
    # Log the top candidates for debugging
    logger.info(f"Top model candidates: {candidates[:3]}")
    
    return candidates[0][1]

def startup_select_model():
    """Populate SELECTED_MODEL_ID and AVAILABLE_MODELS on import/startup."""
    global SELECTED_MODEL_ID, AVAILABLE_MODELS
    try:
        logger.info("Listing available models from Google Generative API...")
        models = list_models(API_KEY)
        AVAILABLE_MODELS = models
        logger.info(f"Found {len(models)} models.")
        chosen = choose_model(models)
        if chosen:
            SELECTED_MODEL_ID = chosen
            logger.info(f"Selected model: {SELECTED_MODEL_ID}")
        elif FALLBACK_MODEL:
            SELECTED_MODEL_ID = FALLBACK_MODEL
            logger.warning(f"No suitable model chosen from ListModels; using FALLBACK_MODEL: {SELECTED_MODEL_ID}")
        else:
            SELECTED_MODEL_ID = None
            logger.warning("No model selected. Set FALLBACK_MODEL or ensure models list contains usable models.")
    except Exception as e:
        logger.exception("Failed to list/select models on startup.")
        if FALLBACK_MODEL:
            SELECTED_MODEL_ID = FALLBACK_MODEL
            logger.info(f"Using FALLBACK_MODEL due to list failure: {SELECTED_MODEL_ID}")
        else:
            SELECTED_MODEL_ID = None

# run selection at import time (Django will import this module at startup)
startup_select_model()

def generate_with_gemini_rest(prompt: str, max_tokens: int = 512):
    """Call :generateContent REST endpoint and return JSON."""
    if not SELECTED_MODEL_ID:
        raise RuntimeError("No SELECTED_MODEL_ID available. Check logs or set FALLBACK_MODEL.")
    model_id = SELECTED_MODEL_ID
    
    # Clean model ID - remove 'models/' prefix if present
    if model_id.startswith('models/'):
        model_id = model_id[7:]  # Remove 'models/' prefix
    
    # Build endpoint with corrected payload format
    url = f"{GOOGLE_BASE}/models/{model_id}:generateContent?key={API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.7
        }
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()

def extract_text_from_response(resp_json: dict) -> str:
    """Extract text from Google Generative AI response with improved parsing."""
    try:
        # Standard Google AI response format
        candidates = resp_json.get("candidates", [])
        if isinstance(candidates, list) and candidates:
            first_candidate = candidates[0]
            if isinstance(first_candidate, dict):
                content = first_candidate.get("content", {})
                if isinstance(content, dict):
                    parts = content.get("parts", [])
                    if isinstance(parts, list) and parts:
                        # Extract text from parts
                        texts = []
                        for part in parts:
                            if isinstance(part, dict) and "text" in part:
                                texts.append(part["text"])
                            elif isinstance(part, str):
                                texts.append(part)
                        if texts:
                            return "\n".join(texts)
                
                # Fallback: check for direct text fields
                for key in ["text", "content", "message"]:
                    if key in first_candidate and isinstance(first_candidate[key], str):
                        return first_candidate[key]
        
        # Legacy format support
        if "text" in resp_json and isinstance(resp_json["text"], str):
            return resp_json["text"]
            
        # Output format support
        output = resp_json.get("output") or resp_json.get("outputs")
        if isinstance(output, list) and output:
            first_output = output[0]
            if isinstance(first_output, dict):
                content = first_output.get("content")
                if isinstance(content, str):
                    return content
                elif isinstance(content, list):
                    texts = []
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            texts.append(item["text"])
                        elif isinstance(item, str):
                            texts.append(item)
                    if texts:
                        return "\n".join(texts)
        
        # Last resort: return string representation
        logger.warning(f"Could not extract text from response: {resp_json}")
        return str(resp_json)
        
    except Exception as e:
        logger.error(f"Error extracting text from response: {e}")
        return str(resp_json)

@csrf_exempt
def health_check(request):
    """Health check endpoint to verify database connectivity"""
    if request.method == 'GET':
        db_connected, db_message = check_database_connection()
        response_data = {
            "status": "healthy" if db_connected else "unhealthy",
            "database": {
                "connected": db_connected,
                "message": db_message
            },
            "selected_model": SELECTED_MODEL_ID,
            "timestamp": timezone.now().isoformat()
        }
        status_code = 200 if db_connected else 503
        return JsonResponse(response_data, status=status_code)
    return JsonResponse({"error": "GET method required"}, status=405)

@csrf_exempt
def chatbot_reply(request):
    if request.method == 'POST':
        try:
            # Check DB connection
            db_connected, db_message = check_database_connection()
            if not db_connected:
                logger.error(f"Database connection failed: {db_message}")
                return JsonResponse({"error": "Database connection failed"}, status=503)

            data = json.loads(request.body)
            prompt = data.get("prompt", "")
            user_id = data.get("user_id", "anonymous")
            session_id = data.get("session_id", "default")

            logger.info(f"Received prompt: {prompt}")
            logger.info(f"User ID: {user_id}, Session ID: {session_id}")

            if not prompt:
                return JsonResponse({"error": "Prompt is required."}, status=400)

            # Save user message to DB (best-effort)
            try:
                user_message = ChatMessage.objects.create(
                    user_id=user_id,
                    text=prompt,
                    sender='user',
                    session_id=session_id
                )
                logger.info(f"Saved user message to DB: {user_message.id}")
            except Exception as e:
                logger.warning(f"Failed to save user message: {e}")

            # Build structured prompt
            structured_prompt = f"""
You are an AI tutor helping a student learn. Please provide a clear, structured response to the following question:

Question: {prompt}

Please format your response with:
1. A clear, concise answer
2. If there are steps, number them clearly (1., 2., 3., etc.)
3. If there are multiple options, list them with bullet points (•)
4. Use **bold** for important terms and concepts
5. Use proper line breaks (\n) to separate paragraphs
6. Keep responses helpful but concise
7. Use clear formatting for lists and steps

Response:
"""

            # Generate via REST
            if not SELECTED_MODEL_ID:
                return JsonResponse({"error": "No model selected on startup. Check server logs or set FALLBACK_MODEL."}, status=500)

            try:
                resp_json = generate_with_gemini_rest(structured_prompt)
                logger.info("Received response from model")
            except requests.HTTPError as http_err:
                logger.exception("HTTP error while calling generateContent")
                try:
                    err_body = http_err.response.json()
                except Exception:
                    err_body = http_err.response.text if http_err.response is not None else str(http_err)
                return JsonResponse({
                    "error": "HTTPError calling generateContent",
                    "status_code": http_err.response.status_code if http_err.response is not None else None,
                    "body": err_body,
                    "selected_model": SELECTED_MODEL_ID
                }, status=502)

            # Extract text safely
            reply = extract_text_from_response(resp_json)

            # Save AI response to DB
            try:
                ai_message = ChatMessage.objects.create(
                    user_id=user_id,
                    text=reply,
                    sender='ai',
                    session_id=session_id
                )
                logger.info(f"Saved AI response to DB: {ai_message.id}")
            except Exception as e:
                logger.warning(f"Failed to save AI response: {e}")

            return JsonResponse({"reply": reply, "selected_model": SELECTED_MODEL_ID})
        except Exception as e:
            logger.exception("Error in chatbot_reply")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Send a POST request with a prompt."})

@csrf_exempt
def get_chat_history(request):
    """Get chat history for a user"""
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id', 'anonymous')
            session_id = request.GET.get('session_id', 'default')

            # Check DB connection
            db_connected, db_message = check_database_connection()
            if not db_connected:
                return JsonResponse({"error": "Database connection failed"}, status=503)

            messages = ChatMessage.objects.filter(
                user_id=user_id,
                session_id=session_id
            ).order_by('timestamp')

            chat_history = []
            for msg in messages:
                chat_history.append({
                    'id': str(msg.id),
                    'text': msg.text,
                    'sender': msg.sender,
                    'timestamp': msg.timestamp.isoformat()
                })

            return JsonResponse({
                "messages": chat_history,
                "count": len(chat_history)
            })
        except Exception as e:
            logger.exception("Error getting chat history")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "GET method required"}, status=405)

@csrf_exempt
def clear_chat(request):
    """Clear chat messages for a specific user and session"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id', 'anonymous')
            session_id = data.get('session_id', 'default')

            # Check DB connection
            db_connected, db_message = check_database_connection()
            if not db_connected:
                return JsonResponse({"error": "Database connection failed"}, status=503)

            deleted_count = ChatMessage.objects.filter(
                user_id=user_id, 
                session_id=session_id
            ).delete()[0]

            logger.info(f"Cleared {deleted_count} messages for user {user_id}, session {session_id}")

            return JsonResponse({
                "status": "success",
                "deleted_count": deleted_count,
                "message": f"Cleared {deleted_count} messages"
            })
        except Exception as e:
            logger.exception("Error clearing chat")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "POST method required"}, status=405)

@csrf_exempt
def get_sessions(request):
    """Get all chat sessions for a user"""
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id', 'anonymous')

            db_connected, db_message = check_database_connection()
            if not db_connected:
                return JsonResponse({"error": "Database connection failed"}, status=503)

            sessions = ChatMessage.objects.filter(
                user_id=user_id
            ).values('session_id').distinct().order_by('-timestamp')

            session_list = []
            for session in sessions:
                session_id = session['session_id']
                first_message = ChatMessage.objects.filter(
                    user_id=user_id,
                    session_id=session_id
                ).order_by('timestamp').first()

                if first_message:
                    session_list.append({
                        'session_id': session_id,
                        'created_at': first_message.timestamp.isoformat(),
                        'message_count': ChatMessage.objects.filter(
                            user_id=user_id,
                            session_id=session_id
                        ).count()
                    })

            return JsonResponse({
                "sessions": session_list,
                "count": len(session_list)
            })
        except Exception as e:
            logger.exception("Error getting sessions")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "GET method required"}, status=405)
