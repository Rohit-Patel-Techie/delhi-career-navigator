"""
Test script for Career Recommendation API improvements
Tests the enhanced API with explanations, disclaimers, and humble tone
"""

import json

# Sample test inputs
test_input = {
    "name": "Rahul Sharma",
    "course_stream": "B.Tech Computer Science",
    "covered_skills": "Python, JavaScript, HTML, CSS, React",
    "career_inclination": "Software Development and AI",
    "time_availability": "Full-time (can dedicate 8+ hours daily)",
    "financial_constraint": False,
    "preferred_language": "english"
}

print("=" * 80)
print("CAREER RECOMMENDATION API - TEST SCRIPT")
print("=" * 80)
print("\nTest Input:")
print(json.dumps(test_input, indent=2))
print("\n" + "=" * 80)

print("\nTesting API with Mock Recommendations...")
print("\nTo test the API, you can:")
print("\n1. Using Curl (from command line):")
curl_command = 'curl -X POST http://localhost:8000/api/recommend/ -H "Content-Type: application/json" -d \'{}\n\''.format(json.dumps(test_input))
print(curl_command)

print("\n\n2. Using Python requests:")
print("""
import requests

url = 'http://localhost:8000/api/recommend/'
response = requests.post(url, json=test_input)
result = response.json()

# Verify new fields exist
print("Disclaimer:", result.get('disclaimer', 'MISSING'))
for rec in result.get('recommendations', []):
    print(f"Rank {rec['rank']}: {rec['pathway_name']}")
    print(f"  Why Recommended: {rec.get('why_recommended', 'MISSING')}")
    print(f"  Fit Score: {rec.get('fit_score', 'MISSING')}")
    print(f"  Considerations: {rec.get('considerations', 'MISSING')}")
""")

print("\n" + "=" * 80)
print("VERIFICATION CHECKLIST")
print("=" * 80)
print("""
When testing, verify:

- Response includes 'disclaimer' field with humble messaging
- Each recommendation has 'why_recommended' field
- Each recommendation has 'fit_score' field  
- Each recommendation has 'considerations' list/array
- Language is humble ("consider", "might", "could") not overconfident
- Considerations mention real trade-offs and challenges
- Why_recommended explains specific fit to user's profile
- Fit scores are qualitative ("Strong fit", "Worth exploring")
""")

print("\n" + "=" * 80)
print("EXPECTED RESPONSE STRUCTURE")
print("=" * 80)
expected = {
  "user_name": "Rahul Sharma",
  "preferred_language": "english",
  "disclaimer": "These are AI-generated suggestions...",
  "recommendations": [
    {
      "rank": 1,
      "pathway_name": "Software Developer",
      "description": "...",
      "why_recommended": "Based on your technical background...",
      "fit_score": "Strong fit",
      "required_skills": ["..."],
      "estimated_salary": "6-15 LPA",
      "growth_prospects": "...",
      "considerations": [
        "Requires continuous learning...",
        "Initial job market can be competitive..."
      ],
      "next_steps": ["..."]
    }
  ]
}
print(json.dumps(expected, indent=2))

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("""
1. Ensure Django server is running: python manage.py runserver
2. Run migrations: python manage.py migrate
3. Test the API endpoint using curl or Python requests
4. Verify all new fields are present in the response
5. Check that tone is humble and encouraging reflection
""")
