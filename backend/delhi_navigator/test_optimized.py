"""
Test with FRESH API key after optimization
"""
import requests

url = "http://127.0.0.1:8000/api/recommend/"
data = {
    "name": "Deepak Bind",
    "course_stream": "BSc CS",
    "covered_skills": "Python, C++",
    "career_inclination": "Tech industry",
    "time_availability": "Part-time",
    "financial_constraint": True,
    "preferred_language": "english"
}

print("🧪 Testing POST /api/recommend/ (AFTER optimization)\n")
print("Expected: Should make ONLY 1 API call now (not 2)\n")

try:
    response = requests.post(url, json=data, timeout=15)
    print(f"✅ Status Code: {response.status_code}\n")
    
    result = response.json()
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        print(f"   Message: {result.get('message', '')}")
    elif "recommendations" in result:
        print(f"✅ SUCCESS! Got {len(result['recommendations'])} recommendations")  
        print(f"   User: {result.get('user_name', 'Unknown')}")
        print(f"   Language: {result.get('preferred_language', 'Unknown')}")
        print(f"   First recommendation: {result['recommendations'][0].get('pathway_name', '')}")
    else:
        print(f"⚠️ Unexpected response structure")
        
except Exception as e:
    print(f"❌ Error: {e}")
