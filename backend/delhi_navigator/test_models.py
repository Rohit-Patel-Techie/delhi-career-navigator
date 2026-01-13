"""
Quick test to see available models in google.genai
"""
from google import genai

# Create client
api_key = "AIzaSyC2uU75Lhd0z_q1DWV7y5Y_G1EtqQ8BuIQ"
client = genai.Client(api_key=api_key)

try:
    # Try to list models
    print("Attempting to list available models...")
    models = client.models.list()
    print("\nAvailable models:")
    for model in models:
        print(f"  - {model.name}")
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying gemini-2.0-flash-exp directly...")
    
try:
    # Try direct generation
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Say hello"
    )
    print(f"\n✅ SUCCESS with gemini-2.0-flash-exp!")
    print(f"Response: {response.text}")
except Exception as e2:
    print(f"❌ Error with gemini-2.0-flash-exp: {e2}")
