#GemAI-Chat

# Smart Conversations, Powered by Django × Google Generative AI

A robust Django-based chatbot backend that integrates with Google's Generative AI models, featuring automatic model discovery, intelligent fallback mechanisms, and comprehensive error handling.

## Features

- **Automatic Model Discovery**: Dynamically selects the best available Google AI model on startup
- **Smart Fallback System**: Uses environment-configured fallback models when auto-discovery fails
- **REST API Integration**: Reliable REST API implementation instead of SDK dependencies
- **Comprehensive Error Handling**: Graceful handling of model unavailability and API errors
- **Chat History Management**: Persistent chat sessions with user and AI message storage
- **Health Monitoring**: Built-in health check endpoints for system monitoring
- **Model Testing Tools**: Management commands for testing AI integration

## Tech Stack

### Frontend

- **React.js** - Modern JavaScript library for building user interfaces
- **TypeScript** - Typed superset of JavaScript for better development experience
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **Vite** - Fast build tool and development server

### Backend

- **Django** - High-level Python web framework
- **Django REST Framework** - Powerful toolkit for building Web APIs
- **Python 3.8+** - Programming language

### Database

- **MySQL** - Relational database management system
- **SQLite** - Lightweight database for development (optional)

### AI Integration

- **Google Generative AI** - Google's AI models for content generation
- **REST API** - Direct API integration for reliable AI communication

### Development Tools

- **Git** - Version control system
- **pip** - Python package manager
- **npm** - Node.js package manager

## Prerequisites

- Python 3.8+
- Node.js 16+
- Django 4.0+
- MySQL 8.0+
- Google AI API Key

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd chatbot-backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:

   ```bash
   GOOGLE_API_KEY=your_google_ai_api_key_here
   FALLBACK_MODEL=gemini-1.5-flash-001
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ```

5. **Run database migrations**

   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Chat Endpoints

**POST /chatbot/reply/**
Send a message to the chatbot and receive an AI response.

Request body:

```json
{
  "prompt": "What is artificial intelligence?",
  "user_id": "user123",
  "session_id": "session456"
}
```

Response:

```json
{
  "reply": "Artificial intelligence (AI) is...",
  "selected_model": "gemini-1.5-flash-001"
}
```

**GET /chatbot/history/**
Retrieve chat history for a user and session.

Query parameters:

- `user_id`: User identifier
- `session_id`: Session identifier

**POST /chatbot/clear/**
Clear chat messages for a specific user and session.

**GET /chatbot/sessions/**
Get all chat sessions for a user.

### System Endpoints

**GET /health/**
Health check endpoint that returns system status and selected AI model.

## Configuration

### Environment Variables

| Variable         | Description                  | Default                |
| ---------------- | ---------------------------- | ---------------------- |
| `GOOGLE_API_KEY` | Google AI API key (required) | -                      |
| `FALLBACK_MODEL` | Fallback model name          | `gemini-1.5-flash-001` |
| `SECRET_KEY`     | Django secret key            | -                      |
| `DEBUG`          | Debug mode                   | `False`                |

### Model Selection

The system automatically selects the best available model based on:

- Support for `generateContent` method
- Model type (prefers Gemini models)
- Version specificity (prefers numbered versions like `001`)
- Stability (avoids experimental models)

## Testing

### Verify AI Integration

Test your Google AI setup:

```bash
python verify_gemini_setup.py
```

### Django Management Commands

Test AI integration through Django:

```bash
python manage.py test_gemini --test-generation
```

List available models:

```bash
python manage.py test_gemini
```

### Health Check

Test system health:

```bash
curl http://localhost:8000/health/
```

## Demo Screenshots

### Chat Interface

![Chat Interface](screenshots/chat-interface.png)
_Main chat interface showing conversation between user and AI_

### API Response

![API Response](screenshots/api-response.png)
_Example API response showing AI-generated content_

### Health Check

![Health Check](screenshots/health-check.png)
_System health check showing selected model and database status_

### Model Selection

![Model Selection](screenshots/model-selection.png)
_Startup logs showing automatic model discovery and selection_

## Project Structure

```
backend/
├── chatbot/
│   ├── management/
│   │   └── commands/
│   │       └── test_gemini.py
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── ai_chatbot/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── db.sqlite3
```

## Error Handling

The system includes comprehensive error handling for:

- **Model Unavailability**: Automatic fallback to configured models
- **API Rate Limits**: Graceful degradation with informative error messages
- **Network Issues**: Timeout handling and retry mechanisms
- **Database Errors**: Non-blocking database operations
- **Invalid Requests**: Proper HTTP status codes and error responses

## Production Deployment

### Security Considerations

- Use environment-specific API keys
- Enable HTTPS in production
- Configure proper CORS settings
- Set up API rate limiting
- Monitor API usage and costs

### Performance Optimization

- Implement response caching
- Use connection pooling
- Monitor database performance
- Set up logging and monitoring
- Configure load balancing

### Environment Setup

```bash
# Production environment variables
GOOGLE_API_KEY=your_production_api_key
FALLBACK_MODEL=gemini-1.5-flash-001
DEBUG=False
SECRET_KEY=your_production_secret_key
DATABASE_URL=postgresql://user:pass@host:port/db
```

## Troubleshooting

### Common Issues

**404 Model Not Found**

- Verify API key has proper permissions
- Check model name in FALLBACK_MODEL
- Run model discovery test

**API Key Errors**

- Ensure GOOGLE_API_KEY is set correctly
- Verify key has Generative Language API access
- Check key format (starts with AIza...)

**Database Connection Issues**

- Verify database configuration
- Run migrations: `python manage.py migrate`
- Check database permissions

### Debug Mode

Enable debug logging:

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Support

For issues and questions:

- Check the troubleshooting section
- Run the verification scripts
- Review Django logs for error details
- Consult Google AI documentation for API issues
