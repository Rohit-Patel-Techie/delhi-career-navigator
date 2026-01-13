"""
Test API error response
"""
import requests
import json

url = "http://localhost:8000/api/recommend/"
data = {
    "name": "Test User",
    "course_stream": "B.Tech CS",
    "covered_skills": "Python",
    "career_inclination": "Tech",
    "time_availability": "Full-time",
    "financial_constraint": False,
    "preferred_language": "english"
}

print("Sending request to API...")
try:
    response = requests.post(url, json=data, timeout=10)
    
    print(f"\n📊 Response Status: {response.status_code}")
    print(f"📝 Response Headers: {dict(response.headers)}")
    print(f"\n📄 Response Body:")
    print(json.dumps(response.json(), indent=2))
    
except requests.exceptions.Timeout:
    print("❌ Request timeout")
except Exception as e:
    print(f"❌ Error: {e}")
