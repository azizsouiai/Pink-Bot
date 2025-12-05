# Chatbruti API Documentation

REST API for the Chatbruti LLM chatbot. Built with FastAPI.

## Quick Start

### Start the API Server

```bash
python -m chatbruti.api_server
```

The server will start on `http://localhost:8000`

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Health Check

**GET** `/health`

Check if the API server and model are ready.

**Response:**
```json
{
  "status": "healthy",
  "backend": "groq",
  "model_name": "openai/gpt-oss-120b",
  "timestamp": "2025-12-05T12:00:00"
}
```

### 2. Send Chat Message

**POST** `/chat`

Send a message to the chatbot and get a response. Maintains conversation history using `session_id`.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "optional-session-id",  // Optional: creates new session if not provided
  "temperature": 1.0,                    // Optional: override default temperature
  "max_tokens": 512,                     // Optional: override default max tokens
  "stream": false                         // Optional: enable streaming (not yet implemented)
}
```

**Response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking...",
  "session_id": "abc123-def456-ghi789",
  "message_count": 3
}
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Python?",
    "session_id": "my-conversation-1"
  }'
```

**Example (JavaScript/Fetch):**
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'What is Python?',
    session_id: 'my-conversation-1'
  })
});

const data = await response.json();
console.log(data.response);
```

### 3. Get Conversation History

**GET** `/conversations/{session_id}`

Retrieve the full conversation history for a session.

**Response:**
```json
{
  "session_id": "abc123-def456-ghi789",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant...",
      "timestamp": "2025-12-05T12:00:00"
    },
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2025-12-05T12:00:01"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I help you?",
      "timestamp": "2025-12-05T12:00:02"
    }
  ],
  "message_count": 3,
  "created_at": "2025-12-05T12:00:00",
  "updated_at": "2025-12-05T12:00:02"
}
```

### 4. Clear Conversation

**POST** `/conversations/{session_id}/clear`

Clear the conversation history for a session (keeps system prompt).

**Response:**
```json
{
  "message": "Conversation abc123 cleared",
  "session_id": "abc123-def456-ghi789"
}
```

### 5. Delete Conversation

**DELETE** `/conversations/{session_id}`

Delete a conversation session entirely.

**Response:**
```json
{
  "message": "Conversation abc123 deleted"
}
```

### 6. List All Conversations

**GET** `/conversations`

List all active conversation sessions.

**Response:**
```json
{
  "sessions": [
    {
      "session_id": "abc123-def456-ghi789",
      "message_count": 5,
      "created_at": "2025-12-05T12:00:00"
    },
    {
      "session_id": "xyz789-abc123-def456",
      "message_count": 2,
      "created_at": "2025-12-05T12:05:00"
    }
  ],
  "total": 2
}
```

## Web Integration Examples

### React/Next.js Example

```javascript
import { useState } from 'react';

function ChatComponent() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);

  const sendMessage = async () => {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: input,
        session_id: sessionId
      })
    });

    const data = await response.json();
    
    // Store session ID for future messages
    if (!sessionId) {
      setSessionId(data.session_id);
    }

    // Update messages
    setMessages(prev => [
      ...prev,
      { role: 'user', content: input },
      { role: 'assistant', content: data.response }
    ]);

    setInput('');
  };

  return (
    <div>
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role}>
            {msg.content}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
```

### Python Client Example

```python
import requests

API_URL = "http://localhost:8000/chat"

def chat(message, session_id=None):
    response = requests.post(API_URL, json={
        "message": message,
        "session_id": session_id
    })
    return response.json()

# First message (creates new session)
result = chat("Hello!")
print(result["response"])
session_id = result["session_id"]

# Continue conversation
result = chat("What did I just say?", session_id=session_id)
print(result["response"])
```

## CORS Configuration

The API is configured to allow CORS from all origins by default. For production, update the CORS settings in `src/chatbruti/api/server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK`: Success
- `404 NOT FOUND`: Resource not found (e.g., session doesn't exist)
- `500 INTERNAL SERVER ERROR`: Server error
- `503 SERVICE UNAVAILABLE`: Model not available

Error responses include a `detail` field with error information:

```json
{
  "detail": "Error generating response: Invalid API key"
}
```

## Configuration

The API uses the same configuration as the CLI:
- Environment variables from `.env` file
- System prompt from `system_prompt.txt`
- Model settings from `src/chatbruti/config/settings.py`

## Production Deployment

For production, use a production ASGI server:

```bash
uvicorn chatbruti.api.server:app --host 0.0.0.0 --port 8000 --workers 4
```

Or use gunicorn with uvicorn workers:

```bash
gunicorn chatbruti.api.server:app -w 4 -k uvicorn.workers.UvicornWorker
```

