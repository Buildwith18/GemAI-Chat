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
# model = genai.GenerativeModel(model_name="models/gemini-pro")  # ✅ Corrected model name

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
#         response = model.generate_content(message.prompt)
#         return {"response": response.text}
#     except Exception as e:
#         return {"error": str(e)}


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env file
load_dotenv()

# Initialize Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ✅ Corrected model name: Use a currently supported model like "gemini-1.5-pro" or "gemini-1.5-flash"
# You might need to check the Google AI for Developers documentation or use genai.list_models()
# to see the exact models available in your region and for your project.
# For example, you could try "gemini-1.5-pro" or "gemini-1.5-flash"
# Let's use a widely available and capable one for demonstration:
# model = genai.GenerativeModel(model_name="gemini-1.5-pro") 
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


# FastAPI setup
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class Message(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_with_gemini(message: Message):
    try:
        response = model.generate_content(message.prompt)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}