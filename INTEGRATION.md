# Chatbruti Widget Integration Guide

This guide explains how the React widget (`widget-UI`) connects to the Chatbruti Python API backend.

## Architecture Overview

```
┌─────────────────────┐
│   React Widget      │  (Frontend - Port 5173)
│   (widget-UI)       │
└──────────┬──────────┘
           │
           │ HTTP POST /chat
           │ JSON: { message, session_id }
           ▼
┌─────────────────────┐
│   FastAPI Server    │  (Backend - Port 8000)
│   (Chatbruti API)   │
└──────────┬──────────┘
           │
           │ Model.generate()
           ▼
┌─────────────────────┐
│   LLM Backend       │  (Groq or Hugging Face)
│   - Groq API        │
│   - Hugging Face    │
└─────────────────────┘
```

## How It Works

### 1. Frontend (React Widget)

The widget is located in `widget-UI/` and consists of:

- **`ChatbotWidget.tsx`**: Main UI component with chat interface
- **`useChatLogic.ts`**: Custom hook that handles API communication
- **`chatConfig.ts`**: Configuration including API URL
- **`ChatMessage.tsx`**: Component for displaying messages

**Key Integration Points:**

1. **API URL Configuration** (`chatConfig.ts`):
   ```typescript
   export const CHAT_API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/chat";
   ```

2. **Message Sending** (`useChatLogic.ts`):
   ```typescript
   const response = await fetch(CHAT_API_URL, {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     body: JSON.stringify({ 
       message: userText,
       session_id: sessionId
     }),
   });
   ```

3. **Response Handling**:
   - The API returns: `{ response: string, session_id: string, message_count: number }`
   - The widget extracts the response text and updates the UI
   - Session ID is stored for conversation history

### 2. Backend (Python API)

The API server is in `src/chatbruti/api/server.py`:

- **Endpoint**: `POST /chat`
- **Request**: `{ message: str, session_id: Optional[str] }`
- **Response**: `{ response: str, session_id: str, message_count: int }`
- **CORS**: Enabled for all origins (configured in `server.py`)

**Key Features:**

- Maintains conversation history per session
- Supports system prompts
- Handles multiple concurrent conversations
- Returns session ID for state management

## Setup Instructions

### Quick Start (Automated)

**On macOS/Linux:**
```bash
cd Chatbruti
./start_integrated.sh
```

**On Windows:**
```bash
cd Chatbruti
start_integrated.bat
```

### Manual Setup

**Step 1: Start the Python API Server**

```bash
cd Chatbruti
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m chatbruti.api_server
```

The API will be available at `http://localhost:8000`

**Step 2: Configure the Widget**

Create a `.env` file in `widget-UI/`:

```bash
cd widget-UI
echo "VITE_API_URL=http://localhost:8000/chat" > .env
```

Or manually create `.env`:
```env
VITE_API_URL=http://localhost:8000/chat
```

**Step 3: Start the Widget**

```bash
cd widget-UI
npm install  # First time only
npm run dev
```

The widget will be available at `http://localhost:5173` (or next available port)

## API Communication Flow

### 1. User Sends Message

```typescript
// Widget sends:
POST http://localhost:8000/chat
{
  "message": "Hello, how are you?",
  "session_id": "abc123"  // Optional, null for first message
}
```

### 2. API Processes Request

```python
# API receives request, loads conversation history
# Generates response using LLM model
# Returns response with session ID
```

### 3. API Returns Response

```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "session_id": "abc123",
  "message_count": 3
}
```

### 4. Widget Updates UI

```typescript
// Widget receives response
// Updates messages state
// Displays response in chat interface
// Stores session_id for next message
```

## Conversation History

The integration maintains conversation context:

1. **First Message**: Widget sends `session_id: null`
   - API creates new session
   - Returns new `session_id`

2. **Subsequent Messages**: Widget sends the stored `session_id`
   - API retrieves conversation history
   - Model has context from previous messages
   - Response maintains conversation flow

3. **Clear Chat**: Widget resets `session_id` to `null`
   - Starts fresh conversation

## CORS Configuration

The API server has CORS enabled in `server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For Production**: Update `allow_origins` to specific domains:
```python
allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
```

## Troubleshooting

### Widget Can't Connect to API

1. **Check API is running**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Verify API URL in `.env`**:
   ```bash
   cat widget-UI/.env
   ```

3. **Check browser console** for CORS errors

4. **Verify ports**:
   - API: `8000`
   - Widget: `5173` (or check terminal output)

### CORS Errors

If you see CORS errors in the browser console:

1. Verify CORS middleware is enabled in `server.py`
2. Check that API server is running
3. Ensure API URL in widget matches actual API address

### Session Not Persisting

- Verify `session_id` is being stored in widget state
- Check that `session_id` is sent with each request
- Verify API is maintaining conversation history

## Testing the Integration

### Test API Directly

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

### Test from Widget

1. Open widget in browser (`http://localhost:5173`)
2. Type a message
3. Check browser DevTools → Network tab
4. Verify request to `/chat` endpoint
5. Check response contains `response` and `session_id`

## Production Deployment

### API Server

1. Set `API_HOST` and `API_PORT` environment variables
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure proper CORS origins
4. Set up reverse proxy (Nginx)

### Widget

1. Build for production:
   ```bash
   cd widget-UI
   npm run build
   ```

2. Deploy `dist/` folder to static hosting
3. Update `.env` with production API URL:
   ```env
   VITE_API_URL=https://api.yourdomain.com/chat
   ```

4. Rebuild after changing `.env`

## Next Steps

- Customize the widget UI in `ChatbotWidget.tsx`
- Modify system prompts in `system_prompt.txt`
- Add authentication if needed
- Implement streaming responses for real-time updates
- Add error handling and retry logic

