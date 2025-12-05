# Troubleshooting Guide - Widget Connection Issues

## Problem: "Can't connect to server" or Error Messages

If you're seeing connection errors in the widget, follow these steps:

### Step 1: Verify API Server is Running

Check if the API server is running:
```bash
curl http://localhost:8000/health
```

You should get a JSON response. If not, start the server:
```bash
cd "/Users/azizsouiai/Documents/NUIT DINFO/Chatbruti"
source venv/bin/activate
python3 -m chatbruti.api_server
```

### Step 2: Check Browser Console

1. Open your browser's Developer Tools (F12 or Cmd+Option+I)
2. Go to the **Console** tab
3. Look for error messages when you send a message
4. Check the **Network** tab to see if requests are being made

Common errors:
- **Failed to fetch**: API server not running or wrong URL
- **CORS error**: CORS configuration issue (should be fixed)
- **405 Method Not Allowed**: Wrong HTTP method (should be POST)
- **404 Not Found**: Wrong endpoint URL

### Step 3: Verify Configuration

Check that `widget-UI/.env` exists and contains:
```env
VITE_API_URL=http://localhost:8000/chat
```

**Important**: After changing `.env`, you must restart the widget dev server!

### Step 4: Restart Widget Dev Server

If you changed the `.env` file or the API server wasn't running when you started the widget:

1. Stop the widget dev server (Ctrl+C)
2. Restart it:
   ```bash
   cd widget-UI
   npm run dev
   ```

### Step 5: Test API Directly

Test the API with curl to verify it's working:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

If this works but the widget doesn't, the issue is with the widget configuration or browser.

### Step 6: Check Network Tab

1. Open browser DevTools → Network tab
2. Send a message in the widget
3. Look for a request to `/chat`
4. Check:
   - **Status**: Should be 200 (not 404, 405, or 500)
   - **Method**: Should be POST
   - **Request URL**: Should be `http://localhost:8000/chat`
   - **Response**: Should contain JSON with `response` and `session_id`

### Step 7: Clear Browser Cache

Sometimes browser cache can cause issues:
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
- Or clear browser cache and reload

### Step 8: Check Port Conflicts

Make sure:
- API server is on port **8000**
- Widget is on port **5173** (or check terminal output)
- No firewall blocking localhost connections

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError: No module named 'chatbruti'"

**Solution:**
```bash
cd "/Users/azizsouiai/Documents/NUIT DINFO/Chatbruti"
source venv/bin/activate
pip install -e .
```

#### Issue: API works with curl but not in widget

**Possible causes:**
1. Widget dev server needs restart after `.env` change
2. Browser cache - try hard refresh
3. CORS issue - check browser console for CORS errors
4. Wrong URL in widget - check browser Network tab

#### Issue: "405 Method Not Allowed"

This means a GET request was sent instead of POST. Check:
- Widget code is using `method: "POST"`
- Browser isn't trying to navigate to the URL

#### Issue: Connection timeout or "Failed to fetch"

**Solutions:**
1. Verify API server is running: `curl http://localhost:8000/health`
2. Check API server logs for errors
3. Verify `.env` has correct URL
4. Restart both API server and widget

### Debug Mode

The widget now logs detailed information to the browser console:
- API URL being used
- Request payload
- Response status
- Error details

Check the browser console (F12 → Console) for these logs.

### Still Not Working?

1. **Check API server logs** - Look for errors in the terminal where the API server is running
2. **Check widget terminal** - Look for errors in the terminal where `npm run dev` is running
3. **Check browser console** - Look for JavaScript errors or network errors
4. **Test with curl** - Verify the API works independently

### Quick Test Checklist

- [ ] API server is running (`curl http://localhost:8000/health` works)
- [ ] Widget `.env` file exists with correct URL
- [ ] Widget dev server was restarted after any `.env` changes
- [ ] Browser console shows no CORS errors
- [ ] Network tab shows POST request to `/chat` with 200 status
- [ ] Both services are running (API on 8000, Widget on 5173)

