# Quick Start Guide - Fixing the Connection Error

## The Problem

If you see the error message **"Oups ! Une erreur s'est produite. Veuillez réessayer."** in the widget, it means the React widget cannot connect to the Python API server.

## The Solution

You need to start the Python API server **before** using the widget.

### Step 1: Start the API Server

Open a terminal and run:

```bash
cd "/Users/azizsouiai/Documents/NUIT DINFO/Chatbruti"
source venv/bin/activate
python -m chatbruti.api_server
```

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!** The API server must stay running.

### Step 2: Verify API is Running

In another terminal, test the API:

```bash
curl http://localhost:8000/health
```

You should get a JSON response with status "healthy".

### Step 3: Use the Widget

Now go back to your browser where the widget is running. Try sending a message again - it should work!

## Running Both Services Together

**Terminal 1 - API Server:**
```bash
cd "/Users/azizsouiai/Documents/NUIT DINFO/Chatbruti"
source venv/bin/activate
python -m chatbruti.api_server
```

**Terminal 2 - React Widget:**
```bash
cd "/Users/azizsouiai/Documents/NUIT DINFO/Chatbruti/widget-UI"
npm run dev
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'chatbruti'"

Install the package:
```bash
cd "/Users/azizsouiai/Documents/NUIT DINFO/Chatbruti"
source venv/bin/activate
pip install -e .
```

### "Connection refused" or CORS errors

1. Make sure the API server is running on port 8000
2. Check that `widget-UI/.env` contains:
   ```
   VITE_API_URL=http://localhost:8000/chat
   ```
3. Restart the widget after changing `.env`

### API starts but model fails to load

Check your `.env` file has the correct configuration:
- For Groq: `GROQ_API_KEY=your_key_here`
- For Hugging Face: Make sure you have enough RAM/VRAM

## Quick Test

Test the API directly:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

If this works, the widget should work too!

