import requests

print("Testing endpoints with server running...\n")

tests = [
    ("GET", "http://127.0.0.1:8000/api/"),
    ("GET", "http://127.0.0.1:8000/api/health/"),
    ("POST", "http://127.0.0.1:8000/api/recommend/", {
        "name": "Test User",
        "course_stream": "B.Tech CS",
        "covered_skills": "Python",
        "career_inclination": "Tech",
        "time_availability": "Full-time",
        "financial_constraint": False,
        "preferred_language": "english"
    }),
]

for test in tests:
    method = test[0]
    url = test[1]
    data = test[2] if len(test) > 2 else None
    
    try:
        if method == "GET":
            r = requests.get(url, timeout=3)
        else:
            r = requests.post(url, json=data, timeout=3)
        
        print(f"{method} {url}")
        print(f"  Status: {r.status_code}")
        print(f"  Response: {r.text[:200]}")
        print()
        
    except Exception as e:
        print(f"{method} {url}")
        print(f"  Error: {e}")
        print()
