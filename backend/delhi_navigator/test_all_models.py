from google import genai
import os
from dotenv import load_dotenv

# Load env
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

# Agar env se nahi mili to hardcoded use karein
if not api_key:
    api_key = "AIzaSyC2uU75Lhd0z_q1DWV7y5Y_G1EtqQ8BuIQ"

print(f"Testing API Key ending in: ...{api_key[-5:]}")

client = genai.Client(api_key=api_key)

print("\n🔍 Google se models dhoondh raha hu (Direct Test Mode)...")

try:
    # 1. List mangwao
    all_models = list(client.models.list())
    print(f"📋 Total Models Found: {len(all_models)}")
    print("-" * 60)
    print(f"{'MODEL NAME (Copy This)':<40} | {'STATUS'}")
    print("-" * 60)

    # 2. Loop through all models
    for m in all_models:
        # Safe name access
        model_name = getattr(m, 'name', str(m))
        
        # Sirf 'gemini' wale models check karenge (PaLM ya others skip)
        if 'gemini' not in model_name.lower():
            continue
            
        # Embedding models ko skip karein (wo text generate nahi karte)
        if 'embedding' in model_name.lower():
            continue

        try:
            # 3. Direct "Hi" bol kar test karein
            # (Attribute check karne ki zaroorat nahi, seedha attack!)
            response = client.models.generate_content(
                model=model_name,
                contents="Hi"
            )
            print(f"✅ {model_name:<40} | WORKING! 🚀")
            
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print(f"⚠️ {model_name:<40} | Busy (429) ⏳")
            elif "404" in error_msg:
                print(f"❌ {model_name:<40} | Not Found")
            elif "not support" in error_msg or "method" in error_msg:
                # Ye model text generation ke liye nahi hoga (e.g. vision only)
                pass 
            else:
                pass # Baki errors ko ignore karein taaki list gandi na ho

    print("-" * 60)
    print("👉 Jo model '✅ WORKING' hai, uska naam copy karke ai_service.py mein lagayein.")

except Exception as e:
    print(f"❌ Script Error: {e}")