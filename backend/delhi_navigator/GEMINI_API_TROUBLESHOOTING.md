# Gemini API Troubleshooting

## Current Issue
**Problem**: API returning "503 UNAVAILABLE - The model is overloaded"

This is happening because:
1. Gemini API has rate limits and usage quotas
2. Model `gemini-2.5-flash` might be experiencing high traffic
3. Our testing has used up available quota

## Solution Options

### Option 1: Wait for Quota Reset
- Free tier API quotas typically reset daily
- Wait a few hours and try again
- Check your API usage at: https://aistudio.google.com/

### Option 2: Try a Different Model
Current: `gemini-2.5-flash` (experiencing overload)

Try these alternatives:
```python
model='gemini-1.5-flash'  # Older, more stable
# OR
model='gemini-pro'  # Classic model
```

### Option 3: Reduce Request Frequency
- Add delays between requests (time.sleep)
- Implement exponential backoff retry logic
- Cache results for similar inputs

### Option 4: Upgrade API Plan
- Consider upgrading to paid tier for higher quotas
- Visit: https://ai.google.dev/pricing

## How to Check Which Source You're Getting

The response now includes a `"source"` field:
- `"source": "gemini-ai"` → Real AI recommendations ✅
- `"source": "mock-fallback"` → Mock data (API unavailable) ⚠️

Check the API response in your application to see this field.

## Testing Command

```bash
python debug_ai_response.py
```

Look for:
- `"source": "gemini-ai"` = Working! 
- `"source": "mock-fallback"` + `"note"` field = API issue
