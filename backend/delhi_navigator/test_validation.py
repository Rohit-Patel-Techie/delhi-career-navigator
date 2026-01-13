"""
Test script to demonstrate AI response validation functionality
"""

from core.ai_service import validate_ai_response

# Test 1: Valid response
print("=" * 60)
print("Test 1: Valid Response")
print("=" * 60)
valid_response = {
    "recommendations": [
        {
            "rank": 1,
            "pathway_name": "Software Developer",
            "description": "Design and develop software applications",
            "why_recommended": "Matches your technical skills",
            "fit_score": "Strong fit",
            "required_skills": ["Python", "JavaScript", "SQL", "Git"],
            "estimated_salary": "₹6-15 LPA",
            "growth_prospects": "Excellent growth in Delhi NCR",
            "considerations": ["Requires continuous learning", "Competitive job market"],
            "next_steps": ["Build portfolio", "Practice coding", "Apply for jobs"]
        },
        {
            "rank": 2,
            "pathway_name": "Data Analyst",
            "description": "Analyze data and create insights",
            "why_recommended": "Good for analytical minds",
            "fit_score": "Moderate fit",
            "required_skills": ["Excel", "SQL", "Python", "Statistics"],
            "estimated_salary": "₹5-12 LPA",
            "growth_prospects": "Very good prospects",
            "considerations": ["May need additional training", "Can be repetitive"],
            "next_steps": ["Learn data tools", "Build projects", "Network"]
        },
        {
            "rank": 3,
            "pathway_name": "Digital Marketing",
            "description": "Execute digital marketing campaigns",
            "why_recommended": "Blends creativity with analytics",
            "fit_score": "Worth exploring",
            "required_skills": ["SEO", "Google Ads", "Social Media", "Analytics"],
            "estimated_salary": "₹4-10 LPA",
            "growth_prospects": "Good growth potential",
            "considerations": ["Results hard to measure", "Constantly changing"],
            "next_steps": ["Get certifications", "Build portfolio", "Join communities"]
        }
    ]
}

is_valid, errors = validate_ai_response(valid_response)
print(f"Valid: {is_valid}")
print(f"Errors: {errors if errors else 'None'}")

# Test 2: Missing field
print("\n" + "=" * 60)
print("Test 2: Missing Required Field")
print("=" * 60)
invalid_response_1 = {
    "recommendations": [
        {
            "rank": 1,
            "pathway_name": "Software Developer",
            # Missing description
            "why_recommended": "Matches your skills",
            "fit_score": "Strong fit",
            "required_skills": ["Python", "JavaScript"],
            "estimated_salary": "₹6-15 LPA",
            "growth_prospects": "Excellent",
            "considerations": ["Learning curve"],
            "next_steps": ["Build portfolio"]
        }
    ]
}

is_valid, errors = validate_ai_response(invalid_response_1)
print(f"Valid: {is_valid}")
print(f"Errors: {errors}")

# Test 3: Invalid fit_score value
print("\n" + "=" * 60)
print("Test 3: Invalid fit_score Value")
print("=" * 60)
invalid_response_2 = {
    "recommendations": [
        {
            "rank": 1,
            "pathway_name": "Software Developer",
            "description": "Develop software",
            "why_recommended": "Good match",
            "fit_score": "Perfect match",  # Invalid value
            "required_skills": ["Python", "JavaScript", "SQL", "Git"],
            "estimated_salary": "₹6-15 LPA",
            "growth_prospects": "Excellent",
            "considerations": ["Learning curve", "Competition"],
            "next_steps": ["Build portfolio", "Practice", "Apply"]
        }
    ]
}

is_valid, errors = validate_ai_response(invalid_response_2)
print(f"Valid: {is_valid}")
print(f"Errors: {errors}")

# Test 4: Wrong number of recommendations
print("\n" + "=" * 60)
print("Test 4: Wrong Number of Recommendations")
print("=" * 60)
invalid_response_3 = {
    "recommendations": [
        {
            "rank": 1,
            "pathway_name": "Software Developer",
            "description": "Develop software",
            "why_recommended": "Good match",
            "fit_score": "Strong fit",
            "required_skills": ["Python", "JavaScript", "SQL", "Git"],
            "estimated_salary": "₹6-15 LPA",
            "growth_prospects": "Excellent",
            "considerations": ["Learning curve", "Competition"],
            "next_steps": ["Build portfolio", "Practice", "Apply"]
        }
        # Only 1 recommendation instead of 3
    ]
}

is_valid, errors = validate_ai_response(invalid_response_3)
print(f"Valid: {is_valid}")
print(f"Errors: {errors}")

# Test 5: Insufficient required_skills
print("\n" + "=" * 60)
print("Test 5: Insufficient Skills")
print("=" * 60)
invalid_response_4 = {
    "recommendations": [
        {
            "rank": 1,
            "pathway_name": "Software Developer",
            "description": "Develop software",
            "why_recommended": "Good match",
            "fit_score": "Strong fit",
            "required_skills": ["Python", "JavaScript"],  # Only 2 skills, needs at least 3
            "estimated_salary": "₹6-15 LPA",
            "growth_prospects": "Excellent",
            "considerations": ["Learning curve", "Competition"],
            "next_steps": ["Build portfolio", "Practice", "Apply"]
        }
    ]
}

is_valid, errors = validate_ai_response(invalid_response_4)
print(f"Valid: {is_valid}")
print(f"Errors: {errors}")

print("\n" + "=" * 60)
print("All validation tests completed!")
print("=" * 60)
