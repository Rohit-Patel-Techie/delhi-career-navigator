import requests
import json

# Test if server is running
print("Testing Django server URLs...")

urls_to_test = [
    "http://127.0.0.1:8000/api/health/",
    "http://127.0.0.1:8000/api/recommend/",
]

for url in urls_to_test:
    try:
        if "health" in url:
            response = requests.get(url, timeout=2)
            print(f"\n✅ GET {url}")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        else:
            # Test POST to recommend
            data = {
                "name": "Test",
                "course_stream": "B.Tech",
                "covered_skills": "Python",
                "career_inclination": "Tech",
                "time_availability": "Full-time",
                "financial_constraint": False,
                "preferred_language": "english"
            }
            response = requests.post(url, json=data, timeout=5)
            print(f"\n📮 POST {url}")
            print(f"   Status: {response.status_code}")
            if response.status_code != 200:
                print(f"   Response: {response.text}")
            else:
                print(f"   Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print(f"\n❌ {url} - Connection refused (server not running?)")
    except Exception as e:
        print(f"\n❌ {url} - Error: {e}")
