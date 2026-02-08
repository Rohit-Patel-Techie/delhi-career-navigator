#!/usr/bin/env python
"""
Cross-platform .env checker script
Yeh script check karega ki .env file sahi load ho raha hai ya nahi

Usage (Windows):
    python check_env.py

Usage (Linux/Mac):
    python3 check_env.py
"""

import os
import sys
from pathlib import Path

def check_env():
    print("=" * 50)
    print("🔍 Environment Variables Checker")
    print("=" * 50)
    
    # Get the script's directory
    script_dir = Path(__file__).resolve().parent
    env_file = script_dir / '.env'
    
    print(f"\n📁 Script location: {script_dir}")
    print(f"📄 Looking for .env at: {env_file}")
    
    # Check if .env file exists
    if not env_file.exists():
        print("\n❌ ERROR: .env file not found!")
        print("   Please create a .env file in the same folder as manage.py")
        return False
    
    print(f"✅ .env file found! Size: {env_file.stat().st_size} bytes")
    
    # Try to load it
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_file, encoding='utf-8')
        print("✅ python-dotenv loaded successfully")
    except ImportError:
        print("\n❌ ERROR: python-dotenv not installed!")
        print("   Run: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"\n❌ ERROR loading .env: {e}")
        return False
    
    # Check key environment variables
    print("\n📋 Environment Variables Status:")
    print("-" * 40)
    
    vars_to_check = [
        ('USE_MOCK_AI', 'Should be "true" for mock mode'),
        ('AI_PROVIDER', 'Optional: "gemini" or "ollama"'),
        ('GEMINI_API_KEY', 'Only needed if AI_PROVIDER=gemini'),
        ('OLLAMA_MODEL', 'Only needed if AI_PROVIDER=ollama'),
    ]
    
    all_ok = True
    for var_name, description in vars_to_check:
        value = os.getenv(var_name, '')
        if value:
            # Mask API keys
            display_value = value[:10] + '...' if 'KEY' in var_name and len(value) > 10 else value
            print(f"  ✅ {var_name} = {display_value}")
        else:
            print(f"  ⚠️  {var_name} = (not set) - {description}")
    
    # Check mock mode specifically
    print("\n🎯 Mode Check:")
    use_mock = os.getenv('USE_MOCK_AI', 'false').lower()
    if use_mock == 'true':
        print("  ✅ MOCK MODE is ENABLED - No API key needed!")
        print("     The app will use fake demo data.")
    else:
        ai_provider = os.getenv('AI_PROVIDER', 'gemini')
        if ai_provider == 'gemini':
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                print(f"  ✅ GEMINI MODE - API key is set")
            else:
                print(f"  ❌ GEMINI MODE but API key is MISSING!")
                all_ok = False
        elif ai_provider == 'ollama':
            print(f"  ✅ OLLAMA MODE - Make sure Ollama is running locally")
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ All checks passed! You can run the server now.")
    else:
        print("⚠️  Some issues found. Please fix them above.")
    print("=" * 50)
    
    return all_ok

if __name__ == '__main__':
    success = check_env()
    sys.exit(0 if success else 1)
