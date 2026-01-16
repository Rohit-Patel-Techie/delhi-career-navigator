"""
Test Provider Switching functionality
"""
import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delhi_navigator.settings')
django.setup()

from core.ai_service import get_career_recommendations

def test_ollama_provider():
    print("🧪 Testing Ollama Provider Integration...")
    
    # Disable MOCK mode explicitly
    os.environ['USE_MOCK_AI'] = 'false'
    
    # Force settings to use Ollama
    # Note: We change os.environ but settings might be already loaded.
    # We might need to mock settings or set usage via env var before import if possible.
    # However, ai_service calls getattr(settings) at runtime, so we can monkeypath settings.
    
    from django.conf import settings
    settings.AI_PROVIDER = 'ollama'
    settings.OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral-nemo:latest') 
    
    print(f"Set AI_PROVIDER to: {settings.AI_PROVIDER}")
    print(f"Using Model: {settings.OLLAMA_MODEL}")
    
    user_input = {
        "name": "Test User",
        "course_stream": "B.Tech CSE",
        "covered_skills": "Python, Django",
        "career_inclination": "Backend Development",
        "time_availability": "Full time",
        "financial_constraint": False,
        "preferred_language": "english"
    }
    
    print("\nRequesting recommendations...")
    try:
        result = get_career_recommendations(user_input, use_mock=False)
        
        if "error" in result:
            print(f"❌ Error returned: {result['error']}")
            print(f"Message: {result.get('message')}")
        else:
            print("✅ Success!")
            print(f"Source: {result.get('source')}")
            print(f"Recommendations count: {len(result.get('recommendations', []))}")
            if result.get('source', '').startswith('ollama'):
                 print("✅ Verified source is Ollama")
            else:
                 print(f"❌ Unexpected source: {result.get('source')}")
                 
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    test_ollama_provider()
