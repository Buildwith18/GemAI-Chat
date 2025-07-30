# 💎 GemAI Chat (WIP)

GemAI Chat is an AI-powered chatbot application currently under development, integrating Google's Gemini API for natural language responses. The backend is powered by Django, and the API has been successfully tested via Postman.

---

## 🚧 Project Status

- ✅ Gemini API key integrated
- ✅ API endpoint tested with Postman
- 🔄 Frontend (React.js) integration in progress
- 🚫 Not yet deployed
- ✅ Working Django backend setup

---

## 🧠 Current Features

- 🔐 Secure backend with Django REST framework
- 🤖 Gemini API integration for AI responses
- 🧪 Postman tested API endpoints

---

## 🧰 Tech Stack

### 🖥️ Backend

- Django
- Django REST Framework
- Google Gemini API (via Python client)

### 📦 Dependencies

- `google-generativeai`
- `djangorestframework`
- `corsheaders`

---

## 📁 Directory Structure

GemAI-Chat/
├── backend/
│ ├── chat/
│ │ ├── views.py # Contains Gemini API logic
│ │ └── urls.py
│ ├── GemAI/ # Django project folder
│ ├── manage.py
└── frontend/ # Will contain React.js frontend

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/GemAI-Chat.git
cd GemAI-Chat

---

2. Backend Setup

cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

---

🔐 Environment Setup
Create a .env or add to settings.py:
GEMINI_API_KEY=your_gemini_api_key

---

📫 Testing API (Postman)
Method: POST

URL: http://localhost:8000/api/gemini/

Headers: Content-Type: application/json

Body:

{
  "question": "What is Django?"
}


Response:

{
  "answer": "Django is a high-level Python web framework..."
}

---

📌 To Do Next
 Build frontend using React.js

 Connect React frontend to Django API

 Add authentication (JWT)

 Add chat history saving

 Add UI styling and responsiveness

---

🙋‍♂️ Author
Made with 💙 by Yugant Trivedi
```
