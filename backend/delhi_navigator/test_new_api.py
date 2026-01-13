"""
Test if new API key is being loaded and working
"""
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

print(f"API Key loaded: {api_key[:20]}...{api_key[-10:] if api_key else 'NOT FOUND'}")
print(f"Key length: {len(api_key) if api_key else 0}")

# Test with google.genai
try:
    from google import genai
    
    client = genai.Client(api_key=api_key)
    
    # Try a simple request
    print("\n🧪 Testing API with simple request...")
    response = client.models.generate_content(
        model='models/gemini-2.0-flash-exp',
        contents="Say hello in one word"
    )
    
    print(f"✅ API WORKS! Response: {response.text}")
    
except Exception as e:
    error_msg = str(e)
    print(f"\n❌ API Error: {error_msg[:300]}")
    
    if "429" in error_msg:
        print("\n⚠️ QUOTA ISSUE - Even new API key is exhausted or IP blocked")
    elif "401" in error_msg or "403" in error_msg:
        print("\n⚠️ AUTHENTICATION ISSUE - API key invalid or not authorized")
    elif "API key" in error_msg:
        print("\n⚠️ API KEY PROBLEM - Check if key is correct")
