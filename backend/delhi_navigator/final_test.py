import requests

url = "http://127.0.0.1:8000/api/recommend/"
data = {
    "name": "Test User",
    "course_stream": "B.Tech CS",
    "covered_skills": "Python",
    "career_inclination": "Tech",
    "time_availability": "Full-time",
    "financial_constraint": False,
    "preferred_language": "english"
}

print("🧪 Testing POST /api/recommend/\n")
try:
    response = requests.post(url, json=data, timeout=10)
    print(f"✅ Status Code: {response.status_code}")
    print(f"📄 Response:\n{response.text[:500]}")
except Exception as e:
    print(f"❌ Error: {e}")
