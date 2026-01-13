import google.generativeai as genai

# ⚠️ YAHAN APNI NAYI 'AI STUDIO' WALI KEY PASTE KAREIN
MY_API_KEY = "AIzaSyC2uU75Lhd0z_q1DWV7y5Y_G1EtqQ8BuIQ" 

genai.configure(api_key=MY_API_KEY)

print("🔍 Google se available models dhundh raha hu...")

try:
    found = False
    for m in genai.list_models():
        # Sirf wo models dikhao jo text generate kar sakte hain
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
            found = True
            
    if not found:
        print("❌ Koi model nahi mila. Shayad API Key mein dikkat hai.")
        
except Exception as e:
    print(f"❌ Error aaya: {e}")