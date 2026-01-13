"""
Debug script to test AI response and identify parsing issues
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delhi_navigator.settings')
django.setup()

from core.ai_service import get_career_recommendations
import json

# Test user input
test_input = {
    "name": "Test User",
    "course_stream": "B.Tech Computer Science",
    "covered_skills": "Python, JavaScript",
    "career_inclination": "Software Development",
    "time_availability": "Full-time",
    "financial_constraint": False,
    "preferred_language": "english"
}

print("=" * 70)
print("TESTING AI RESPONSE GENERATION")
print("=" * 70)
print(f"\nTest Input:")
print(json.dumps(test_input, indent=2))
print("\n" + "=" * 70)

# Get recommendations
result = get_career_recommendations(test_input, use_mock=False)

print("\nResult:")
print("=" * 70)
print(json.dumps(result, indent=2, ensure_ascii=False))
print("=" * 70)

# Check for issues
if "note" in result:
    print(f"\n⚠️  WARNING: {result['note']}")
    
if "error" in result:
    print(f"\n❌ ERROR: {result['error']}")
    
if "recommendations" in result and len(result["recommendations"]) == 3:
    print("\n✅ SUCCESS: Got 3 valid recommendations!")
else:
    print("\n❌ FAILED: Did not get 3 valid recommendations")
