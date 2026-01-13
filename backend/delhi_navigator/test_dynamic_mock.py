"""
Test script to demonstrate dynamic mock recommendations based on user input
"""

from core.ai_service import get_mock_recommendations
import json

print("=" * 80)
print("DYNAMIC MOCK RECOMMENDATIONS TEST")
print("=" * 80)

# Test 1: Student with financial constraints and Python skills
print("\n" + "=" * 80)
print("Test 1: Budget-Conscious Computer Science Student with Python Skills")
print("=" * 80)
user_input_1 = {
    "name": "Rahul",
    "course_stream": "Computer Science",
    "covered_skills": "Python, HTML, CSS",
    "career_inclination": "Software Development",
    "time_availability": "Full-time available",
    "financial_constraint": True,
    "preferred_language": "english"
}

result_1 = get_mock_recommendations(user_input_1)
print(f"User: {result_1['user_name']}")
for rec in result_1['recommendations']:
    print(f"\n{rec['rank']}. {rec['pathway_name']} ({rec['fit_score']})")
    print(f"   Salary: {rec['estimated_salary']}")
    print(f"   Why: {rec['why_recommended'][:120]}...")
    print(f"   Next Steps: {rec['next_steps'][0]}")

# Test 2: Creative student with part-time availability
print("\n" + "=" * 80)
print("Test 2: Design Student with Limited Time Availability")
print("=" * 80)
user_input_2 = {
    "name": "Priya",
    "course_stream": "Graphic Design",
    "covered_skills": "Photoshop, Illustrator, Figma",
    "career_inclination": "UI/UX Design and Creative Work",
    "time_availability": "Part-time, few hours per day",
    "financial_constraint": False,
    "preferred_language": "english"
}

result_2 = get_mock_recommendations(user_input_2)
print(f"User: {result_2['user_name']}")
for rec in result_2['recommendations']:
    print(f"\n{rec['rank']}. {rec['pathway_name']} ({rec['fit_score']})")
    print(f"   Salary: {rec['estimated_salary']}")
    print(f"   Why: {rec['why_recommended'][:120]}...")
    print(f"   Considerations: {rec['considerations'][2]}")

# Test 3: Business student with budget constraints
print("\n" + "=" * 80)
print("Test 3: BBA Student with Financial Constraints")
print("=" * 80)
user_input_3 = {
    "name": "Amit",
    "course_stream": "BBA (Business Administration)",
    "covered_skills": "Excel, Communication, Presentations",
    "career_inclination": "Business Analysis and Management",
    "time_availability": "Full-time",
    "financial_constraint": True,
    "preferred_language": "english"
}

result_3 = get_mock_recommendations(user_input_3)
print(f"User: {result_3['user_name']}")
for rec in result_3['recommendations']:
    print(f"\n{rec['rank']}. {rec['pathway_name']} ({rec['fit_score']})")
    print(f"   Salary: {rec['estimated_salary']}")
    print(f"   Skills Referenced: ", end="")
    # Show which skills were matched
    matched = []
    for skill in rec['required_skills']:
        if skill.lower() in user_input_3['covered_skills'].lower():
            matched.append(skill)
    print(matched if matched else "None")
    print(f"   Why: {rec['why_recommended']}")

# Test 4: Content writing enthusiast with limited time
print("\n" + "=" * 80)
print("Test 4: English Major Interested in Writing (Part-time)")
print("=" * 80)
user_input_4 = {
    "name": "Sneha",
    "course_stream": "English Literature",
    "covered_skills": "Writing, Research, Communication",
    "career_inclination": "Content Writing and Creative Writing",
    "time_availability": "Limited availability, part-time",
    "financial_constraint": True,
    "preferred_language": "english"
}

result_4 = get_mock_recommendations(user_input_4)
print(f"User: {result_4['user_name']}")
for rec in result_4['recommendations']:
    print(f"\n{rec['rank']}. {rec['pathway_name']} ({rec['fit_score']})")
    print(f"   Salary: {rec['estimated_salary']}")
    print(f"   Why: {rec['why_recommended']}")
    print(f"   Budget Consideration: {rec['considerations'][2]}")
    print(f"   Next Step: {rec['next_steps'][0]}")

# Test 5: Data Analytics interest with no constraints
print("\n" + "=" * 80)
print("Test 5: Statistics Student with No Financial Constraints")
print("=" * 80)
user_input_5 = {
    "name": "Vikram",
    "course_stream": "Statistics",
    "covered_skills": "Excel, Python, SQL, Data Analysis",
    "career_inclination": "Data Analytics and Business Intelligence",
    "time_availability": "Full-time available",
    "financial_constraint": False,
    "preferred_language": "english"
}

result_5 = get_mock_recommendations(user_input_5)
print(f"User: {result_5['user_name']}")
for rec in result_5['recommendations']:
    print(f"\n{rec['rank']}. {rec['pathway_name']} ({rec['fit_score']})")
    print(f"   Salary: {rec['estimated_salary']}")
    print(f"   Required Skills: {', '.join(rec['required_skills'])}")
    print(f"   Why: {rec['why_recommended']}")
    print(f"   Next Step: {rec['next_steps'][0]}")

print("\n" + "=" * 80)
print("All dynamic mock recommendation tests completed!")
print("=" * 80)
