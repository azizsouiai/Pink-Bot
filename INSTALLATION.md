# Complete Installation Guide

This guide will help you set up both the Python backend and React widget.

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and **npm** (for React widget)
- **Groq API Key** (get one at https://console.groq.com/)

## Step-by-Step Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/azizsouiai/Pink-Bot.git
cd Pink-Bot
```

### Step 2: Set Up Python Backend

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```
   ⚠️ **This step is required!** Without it, Python won't find the `chatbruti` module.

4. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   BACKEND=groq
   MODEL_NAME=openai/gpt-oss-120b
   ```

5. **Test the backend:**
   ```bash
   python -m chatbruti.main --model-info
   ```

### Step 3: Set Up React Widget

1. **Navigate to widget directory:**
   ```bash
   cd widget-UI
   ```
   
   If the widget is in a separate location:
   ```bash
   cd /path/to/widget-UI
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Configure API URL:**
   Create `.env` file:
   ```bash
   echo "VITE_API_URL=http://localhost:8000/chat" > .env
   ```
   
   Or manually create `.env`:
   ```env
   VITE_API_URL=http://localhost:8000/chat
   ```

4. **Test the widget:**
   ```bash
   npm run dev
   ```

### Step 4: Run Both Services

**Terminal 1 - Start Python API:**
```bash
cd Pink-Bot
source venv/bin/activate
python -m chatbruti.api_server
```
You should see: `Starting Chatbruti API server on http://0.0.0.0:8000`

**Terminal 2 - Start React Widget:**
```bash
cd widget-UI
npm run dev
```
You should see: `Local: http://localhost:5173/`

**Open your browser** and go to `http://localhost:5173` to see the widget!

## Verification

### Test Python API

```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "backend": "groq",
  "model_name": "openai/gpt-oss-120b"
}
```

### Test Widget Connection

1. Open browser to widget URL (usually `http://localhost:5173`)
2. Open browser DevTools (F12) → Console tab
3. Send a message in the widget
4. Check console for any errors

## Troubleshooting

### Python: "ModuleNotFoundError: No module named 'chatbruti'"

**Solution:** Run `pip install -e .` in the project root directory.

### Widget: "Oups ! Une erreur s'est produite"

**Possible causes:**
1. API server not running - Start it with `python -m chatbruti.api_server`
2. Wrong API URL - Check `.env` file in widget-UI directory
3. CORS error - API should allow all origins by default
4. API key invalid - Check your `.env` file in Chatbruti directory

### Port Already in Use

**Python API (port 8000):**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**React Widget (port 5173):**
Vite will automatically use the next available port. Check terminal output.

## Next Steps

- Customize the system prompt: Edit `system_prompt.txt`
- Adjust API settings: Edit `.env` file
- Build widget for production: `cd widget-UI && npm run build`
- Deploy API: See API_DOCS.md for production deployment

## Quick Commands Reference

**Start API:**
```bash
cd Pink-Bot && source venv/bin/activate && python -m chatbruti.api_server
```

**Start Widget:**
```bash
cd widget-UI && npm run dev
```

**CLI Usage:**
```bash
cd Pink-Bot && source venv/bin/activate && python -m chatbruti.main --interactive
```

