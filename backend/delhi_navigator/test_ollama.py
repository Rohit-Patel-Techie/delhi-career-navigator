"""
Test connection to local Ollama instance
"""
import requests
import json
import os
import time

def test_ollama_connection():
    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'mistral')
    
    print(f"Testing Ollama connection at {base_url} with model {model}...")
    
    try:
        # Test 1: Check version/tags
        print(f"1. Checking tags endpoint...")
        response = requests.get(f"{base_url}/api/tags")
        if response.status_code == 200:
            print("✅ Ollama is running!")
            models = response.json().get('models', [])
            print(f"   Available models: {[m['name'] for m in models]}")
            
            # Check if requested model exists
            model_exists = any(m['name'].startswith(model) for m in models)
            if not model_exists:
                print(f"⚠️  Warning: Model '{model}' not found in list. Use 'ollama pull {model}' to get it.")
        else:
            print(f"❌ Failed to reach tags endpoint. Status: {response.status_code}")
            return

        # Test 2: Simple generation
        print(f"\n2. Testing generation...")
        start_time = time.time()
        
        payload = {
            "model": model,
            "prompt": "Say 'Ollama is working' in JSON format like {\"status\": \"ok\"}",
            "stream": False,
            "format": "json"
        }
        
        response = requests.post(f"{base_url}/api/generate", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            duration = time.time() - start_time
            print(f"✅ Generation successful in {duration:.2f}s")
            print(f"   Response: {result.get('response')}")
        else:
            print(f"❌ Generation failed. Status: {response.status_code}")
            print(f"   Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection refused at {base_url}")
        print("   Is Ollama running? Try 'ollama serve' in a terminal.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_ollama_connection()
