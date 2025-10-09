# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# import google.generativeai as genai

# # Load .env file
# load_dotenv()

# # Initialize Gemini
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # ✅ Corrected model name: Use a currently supported model like "gemini-1.5-pro" or "gemini-1.5-flash"
# # You might need to check the Google AI for Developers documentation or use genai.list_models()
# # to see the exact models available in your region and for your project.
# # For example, you could try "gemini-1.5-pro" or "gemini-1.5-flash"
# # Let's use a widely available and capable one for demonstration:
# # model = genai.GenerativeModel(model_name="gemini-1.5-pro") 
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")


# # FastAPI setup
# app = FastAPI()

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all for development
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Request body schema
# class Message(BaseModel):
#     prompt: str

# @app.post("/chat")
# async def chat_with_gemini(message: Message):
#     try:
#         print ("Hello")
#         response = model.generate_content(message.prompt)
#         return {"response": response.text}
#     except Exception as e:
#         return {"error": str(e)}



# filename: main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import requests
import logging

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")  # ensure this is set
# Optional: set a fallback model name (only used if ListModels doesn't find anything appropriate)
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "")  # e.g. "gemini-2.5-flash"

if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in your environment (.env) before running.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gemini-fastapi")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    prompt: str

# Globals populated on startup
SELECTED_MODEL_ID: str | None = None
AVAILABLE_MODELS: list = []

GOOGLE_BASE = "https://generativelanguage.googleapis.com/v1beta"

def list_models(api_key: str) -> list:
    """Call ListModels and return the raw 'models' array (or empty list)."""
    url = f"{GOOGLE_BASE}/models?key={api_key}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    # Google may return models under "models" key
    return data.get("models", [])

def choose_model(models: list) -> str | None:
    """
    Choose the best model that appears to support generateContent.
    Heuristics:
      - prefer model ids that include 'gemini' or 'flash' or '2.5' / '2.1' etc.
      - prefer ones that list supported methods including 'generateContent' (if available).
    """
    # inspect common fields safely
    # We'll look for "name" (full resource) or "model" or "modelId"
    candidates = []
    for m in models:
        # normalize name/id
        name = m.get("name") or m.get("model") or m.get("modelId") or ""
        # check for methods field
        methods = m.get("supportedMethods") or m.get("supported_methods") or m.get("availableMethods") or m.get("supportedFeatures") or []
        methods_text = " ".join(methods).lower() if isinstance(methods, list) else str(methods).lower()
        # prefer ones that explicitly list generateContent
        supports_generate = "generatecontent" in methods_text or "generate_content" in methods_text or "generatecontent" in str(m).lower()
        # prefer gemini names
        is_gemini = "gemini" in name.lower()
        # score heuristics
        score = 0
        if supports_generate:
            score += 10
        if is_gemini:
            score += 5
        if "flash" in name.lower():
            score += 3
        if "2.5" in name.lower() or "2.1" in name.lower() or "2.0" in name.lower():
            score += 2
        candidates.append((score, name, supports_generate, methods))
    # sort by score desc, prefer non-empty name
    candidates = [c for c in candidates if c[1]]
    if not candidates:
        return None
    candidates.sort(reverse=True, key=lambda t: t[0])
    # return the top name
    return candidates[0][1]

@app.on_event("startup")
def startup_event():
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
            logger.info(f"No obvious model chosen from list; using FALLBACK_MODEL: {SELECTED_MODEL_ID}")
        else:
            SELECTED_MODEL_ID = None
            logger.warning("No model selected. You must set FALLBACK_MODEL or ensure models list contains usable models.")
    except Exception as e:
        logger.exception("Failed to list or select models:")
        if FALLBACK_MODEL:
            SELECTED_MODEL_ID = FALLBACK_MODEL
            logger.info(f"Using FALLBACK_MODEL despite list failure: {SELECTED_MODEL_ID}")
        else:
            SELECTED_MODEL_ID = None

def generate_with_rest(model_id: str, prompt_text: str, api_key: str, max_tokens: int = 512) -> dict:
    """
    Call the REST generateContent endpoint for a model.
    We attempt a message-based prompt format that matches common GA examples:
      { "prompt": { "messages": [{"author":"user","content":"..."}] }, "maxOutputTokens": ... }
    This function returns the parsed JSON response (or raises on HTTP error).
    """
    url = f"{GOOGLE_BASE}/models/{model_id}:generateContent?key={api_key}"
    payload = {
        "prompt": {
            "messages": [
                {"author": "user", "content": prompt_text}
            ]
        },
        "maxOutputTokens": max_tokens
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()

def extract_text_from_response(resp_json: dict) -> str:
    """
    Attempt to extract model text from multiple possible response shapes:
      - resp['candidates'][0]['content']
      - resp['output'][0]['content'][0]['text']
      - resp['output'][0]['candidates'][0]['content']
      - resp['candidates'][0]['message'] etc.
    """
    # candidate-style (common)
    if isinstance(resp_json.get("candidates"), list) and resp_json["candidates"]:
        first = resp_json["candidates"][0]
        # different keys used in different versions
        for k in ("content", "output", "message", "text"):
            if k in first and isinstance(first[k], str):
                return first[k]
        # sometimes content is list of parts
        parts = first.get("content") or first.get("output")
        if isinstance(parts, list):
            # join text parts if needed
            texts = []
            for p in parts:
                if isinstance(p, dict) and "text" in p:
                    texts.append(p["text"])
                elif isinstance(p, str):
                    texts.append(p)
            if texts:
                return "\n".join(texts)
    # output-style
    out = resp_json.get("output") or resp_json.get("outputs")
    if isinstance(out, list) and out:
        first = out[0]
        # check for 'content' list
        content = first.get("content") if isinstance(first, dict) else None
        if isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    texts.append(item["text"])
                elif isinstance(item, str):
                    texts.append(item)
            if texts:
                return "\n".join(texts)
        # fallback to 'text' field
        if isinstance(first, dict) and "text" in first:
            return first["text"]
    # message-style
    if resp_json.get("message") and isinstance(resp_json["message"], dict):
        return resp_json["message"].get("content", "")
    # fall back to full json string (last resort)
    return str(resp_json)

@app.post("/chat")
async def chat_with_gemini(message: Message):
    if not SELECTED_MODEL_ID:
        return {
            "error": "No model selected at startup. Check server logs or set FALLBACK_MODEL env var."
        }
    try:
        logger.info(f"Using model {SELECTED_MODEL_ID} to generate content.")
        resp_json = generate_with_rest(SELECTED_MODEL_ID, message.prompt, API_KEY)
        text = extract_text_from_response(resp_json)
        return {"response": text, "raw": resp_json}
    except requests.HTTPError as http_err:
        # surface status and body for diagnostics
        logger.exception("HTTP error while calling generateContent")
        try:
            body = http_err.response.json()
        except Exception:
            body = http_err.response.text if http_err.response is not None else str(http_err)
        return {
            "error": "HTTPError calling generateContent",
            "status_code": http_err.response.status_code if http_err.response is not None else None,
            "body": body,
        }
    except Exception as e:
        logger.exception("Unexpected error while generating content")
        return {"error": str(e)}
