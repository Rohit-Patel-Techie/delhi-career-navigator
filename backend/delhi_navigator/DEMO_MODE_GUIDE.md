# Delhi Career Navigator - Quick Demo Setup

## Problem: API Quota Exhausted

Your Gemini API free tier quota is exhausted. Here are your options:

### ✅ OPTION 1: Demo Mode (RECOMMENDED)

Enable mock responses for unlimited demo usage:

**In `.env` file**:
```
USE_MOCK_AI=true
```

**Benefits**:
- ✅ No API quota usage
- ✅ Unlimited requests
- ✅ High-quality personalized recommendations
- ✅ Perfect for hackathon judges
- ✅ Instant response (no API latency)

**Mocks are VERY good** - they:
- Use the user's actual name, skills, course
- Match their constraints (time/budget)
- Provide Delhi-specific market data
- Follow the same mentoring tone

---

### Option 2: Wait for Quota Reset

- Timeline: 12-24 hours
- Free tier resets daily

---

### Option 3: Upgrade API Plan

Visit: https://aistudio.google.com/
Cost: ~₹10-50 per demo

---

## How to Enable Demo Mode NOW

1. Open `.env` file
2. Change line: `USE_MOCK_AI=false` → `USE_MOCK_AI=true`
3. Save file
4. Server auto-reloads
5. ✅ Demo ready!

**Recommendation**: Use mock mode for hackathon demo!
