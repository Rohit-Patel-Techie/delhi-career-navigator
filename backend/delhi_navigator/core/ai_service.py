"""
AI Service for Career Pathway Recommendations
Uses Google Gemini API with Delhi market data to suggest top 3 career pathways
"""

import json
import os
import re
import time
import logging
import hashlib
from pathlib import Path
from django.conf import settings

# Setup logger
logger = logging.getLogger(__name__)

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def load_delhi_market_data():
    """Load Delhi market demand data from JSON file"""
    data_path = Path(__file__).parent / 'data' / 'delhi_market_data.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_prompt(user_input: dict, market_data: dict, language: str = 'english') -> str:
    """Build the AI prompt with user input and market data"""
    
    language_instruction = ""
    if language == 'hindi':
        language_instruction = "IMPORTANT: Respond entirely in Hindi (Devanagari script). All descriptions, explanations, and next steps should be in Hindi."
    else:
        language_instruction = "Respond in clear, professional English."
    
    prompt = f"""
You are a friendly, experienced career mentor who knows the Delhi NCR job market inside-out. 
You're having a personal conversation with {user_input.get('name', 'a student')}, helping them figure out their career path.

MENTORING STYLE:
- Talk directly to them using "you" and "I" (conversational, not formal)
- Be warm, encouraging, and realistic (like a supportive older friend/mentor)
- Use casual language mixed with professionalism (e.g., "Look, here's the deal..." "I think you'd do really well in...")
- Give SPECIFIC advice based on THEIR situation - not generic statements
- Be honest about challenges but keep it motivating
- Sound like you're sitting across from them having chai and discussing their future

## About {user_input.get('name', 'the Student')}:
- Currently studying: {user_input.get('course_stream', 'Not specified')}
- Skills they already have: {user_input.get('covered_skills', 'Not specified')}
- What interests them: {user_input.get('career_inclination', 'Not specified')}
- Time they can dedicate: {user_input.get('time_availability', 'Not specified')}
- Budget situation: {'On a tight budget, needs affordable options' if user_input.get('financial_constraint', False) else 'Can invest in courses/training if needed'}

## Delhi NCR Job Market Reality:
{json.dumps(market_data, indent=2)}

## Your Mentoring Task:
Based on what you know about {user_input.get('name', 'them')}, suggest 3 career paths that make sense.

For EACH path, write like you're explaining to them personally:

1. **Pathway Name**: The career/role
2. **Description**: What the job actually involves (2-3 sentences, conversational)
3. **Why I'm Suggesting This For You**: Explain WHY this fits THEM specifically - mention their course ({user_input.get('course_stream', '')}), their skills ({user_input.get('covered_skills', '')}), their interests ({user_input.get('career_inclination', '')}), and constraints. Be SPECIFIC, not generic. (Write like: "Look, with your {user_input.get('course_stream', '')} background and those Python skills you mentioned...")
4. **Fit Score**: "Strong fit" / "Moderate fit" / "Worth exploring"
5. **Required Skills**: 4-6 skills they'll need (mention which ones they already have!)
6. **Salary Range**: What they can expect in Delhi NCR
7. **Growth Potential**: Real talk about opportunities in Delhi
8. **Real Talk - Challenges**: Be honest about 2-3 difficulties or trade-offs. Don't sugarcoat, but keep it balanced.
9. **Your 30-Day Action Plan**: 3-4 specific, actionable steps to start THIS MONTH (not vague advice)

CRITICAL: Write "why_recommended", "considerations", and "next_steps" in FIRST PERSON, talking DIRECTLY to {user_input.get('name', 'them')}.
Examples:
- "Given YOUR background in..." not "Given the user's background..."
- "YOU already have Python skills which..." not "The user has..."
- "I suggest YOU start by..." not "They should start..."

{language_instruction}

## Response Format (STRICT JSON):
{{
    "recommendations": [
        {{
            "rank": 1,
            "pathway_name": "Career Title",
            "description": "What this role involves...",
            "why_recommended": "Look, with YOUR [specific course/skills], I think this could work really well because... [specific match to THEIR situation]",
            "fit_score": "Strong fit",
            "required_skills": ["skill1", "skill2", "skill3", "skill4"],
            "estimated_salary": "₹X-Y LPA",
            "growth_prospects": "Honest market outlook...",
            "considerations": [
                "Real challenge 1",
                "Trade-off 2",
                "Something to know 3"
            ],
            "next_steps": ["Specific action 1", "Specific action 2", "Specific action 3"]
        }},
        {{ "rank": 2, ... }},
        {{ "rank": 3, ... }}
    ]
}}

Only return the JSON object, no additional text.
"""
    return prompt

def parse_ai_response(response_text: str) -> dict:
    """Parse the AI response and extract recommendations"""
    try:
        # 1. Clean up markdown code blocks if present
        clean_text = re.sub(r'```json\s*|\s*```', '', response_text).strip()
        
        # 2. Try to find JSON object (fixed regex to avoid SyntaxWarning)
        json_match = re.search(r'\{[\s\S]*\}', clean_text)
        if json_match:
            parsed = json.loads(json_match.group())
            return parsed
        
        return {"error": "Could not parse AI response"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parsing error: {str(e)}"}


def validate_ai_response(response_data: dict) -> tuple[bool, list[str]]:
    """
    Validate AI response structure and content
    
    Args:
        response_data: The parsed JSON response from AI
        
    Returns:
        Tuple of (is_valid: bool, errors: list[str])
    """
    errors = []
    
    # Check if error is present in response
    if "error" in response_data:
        errors.append(f"Response contains error: {response_data['error']}")
        return False, errors
    
    # Check for recommendations array
    if "recommendations" not in response_data:
        errors.append("Missing 'recommendations' field")
        return False, errors
    
    recommendations = response_data["recommendations"]
    
    # Check if recommendations is a list
    if not isinstance(recommendations, list):
        errors.append("'recommendations' must be a list")
        return False, errors
    
    # Check for exactly 3 recommendations
    if len(recommendations) != 3:
        errors.append(f"Expected exactly 3 recommendations, got {len(recommendations)}")
    
    # Required fields for each recommendation
    required_fields = {
        "rank": int,
        "pathway_name": str,
        "description": str,
        "why_recommended": str,
        "fit_score": str,
        "required_skills": list,
        "estimated_salary": str,
        "growth_prospects": str,
        "considerations": list,
        "next_steps": list
    }
    
    # Validate each recommendation
    for idx, rec in enumerate(recommendations, 1):
        if not isinstance(rec, dict):
            errors.append(f"Recommendation {idx} is not a dictionary")
            continue
        
        # Check required fields
        for field, expected_type in required_fields.items():
            if field not in rec:
                errors.append(f"Recommendation {idx}: Missing required field '{field}'")
            elif not isinstance(rec[field], expected_type):
                errors.append(
                    f"Recommendation {idx}: Field '{field}' should be {expected_type.__name__}, "
                    f"got {type(rec[field]).__name__}"
                )
        
        # Validate rank value
        if "rank" in rec:
            if rec["rank"] not in [1, 2, 3]:
                errors.append(f"Recommendation {idx}: Invalid rank {rec['rank']}, must be 1, 2, or 3")
        
        # Validate fit_score values
        if "fit_score" in rec:
            valid_scores = ["Strong fit", "Moderate fit", "Worth exploring"]
            if rec["fit_score"] not in valid_scores:
                errors.append(
                    f"Recommendation {idx}: Invalid fit_score '{rec['fit_score']}', "
                    f"must be one of: {', '.join(valid_scores)}"
                )
        
        # Validate list fields have content
        if "required_skills" in rec and isinstance(rec["required_skills"], list):
            if len(rec["required_skills"]) < 3:
                errors.append(f"Recommendation {idx}: 'required_skills' should have at least 3 items")
            if len(rec["required_skills"]) > 8:
                errors.append(f"Recommendation {idx}: 'required_skills' should have at most 8 items")
        
        if "considerations" in rec and isinstance(rec["considerations"], list):
            if len(rec["considerations"]) < 2:
                errors.append(f"Recommendation {idx}: 'considerations' should have at least 2 items")
        
        if "next_steps" in rec and isinstance(rec["next_steps"], list):
            if len(rec["next_steps"]) < 3:
                errors.append(f"Recommendation {idx}: 'next_steps' should have at least 3 items")
        
        # Validate string fields are not empty
        for field in ["pathway_name", "description", "why_recommended", "estimated_salary", "growth_prospects"]:
            if field in rec and isinstance(rec[field], str):
                if not rec[field].strip():
                    errors.append(f"Recommendation {idx}: Field '{field}' cannot be empty")
    
    is_valid = len(errors) == 0
    return is_valid, errors


# Simple in-memory cache for API responses (saves quota!)
_response_cache = {}
_cache_timeout = 300  # 5 minutes

def _get_cache_key(user_input: dict) -> str:
    """Generate cache key from user input"""
    import hashlib
    import json
    # Create deterministic key from input
    key_data = json.dumps(user_input, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()


def get_ollama_recommendations(user_input: dict, prompt: str, max_retries: int = 3) -> dict:
    """
    Get recommendations from Ollama API with automatic retry logic.
    
    Args:
        user_input: User input data
        prompt: The prompt to send to Ollama
        max_retries: Maximum number of retry attempts (default: 3)
    """
    if not REQUESTS_AVAILABLE:
        return {
            "error": "Dependency missing",
            "message": "The 'requests' library is required for Ollama integration."
        }
        
    base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
    model = getattr(settings, 'OLLAMA_MODEL', 'mistral')
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }
    
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"🔄 Ollama attempt {attempt}/{max_retries}")
            
            response = requests.post(f"{base_url}/api/generate", json=payload, timeout=300)
            
            if response.status_code != 200:
                last_error = {
                    "error": "Ollama API error",
                    "message": f"Ollama returned status {response.status_code}: {response.text}"
                }
                logger.warning(f"⚠️ Attempt {attempt} failed: HTTP {response.status_code}")
                if attempt < max_retries:
                    wait_time = attempt * 5  # 5s, 10s, 15s
                    logger.info(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                continue
                
            result = response.json()
            response_text = result.get('response', '')
            
            # Parse and validate
            parsed_result = parse_ai_response(response_text)
            is_valid, validation_errors = validate_ai_response(parsed_result)
            
            if not is_valid:
                last_error = {
                    "error": "Ollama response validation failed",
                    "message": f"Invalid format: {'; '.join(validation_errors[:3])}"
                }
                logger.warning(f"⚠️ Attempt {attempt} failed: Validation error")
                if attempt < max_retries:
                    wait_time = attempt * 5
                    logger.info(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                continue
                
            # Success!
            logger.info(f"✅ Ollama succeeded on attempt {attempt}")
            parsed_result["source"] = f"ollama-{model}"
            parsed_result["attempts"] = attempt
            return parsed_result
            
        except requests.exceptions.Timeout:
            last_error = {
                "error": "Ollama timeout",
                "message": f"Request timed out after 300s (attempt {attempt}/{max_retries})"
            }
            logger.warning(f"⚠️ Attempt {attempt} timed out")
            if attempt < max_retries:
                wait_time = attempt * 10  # Longer wait for timeouts
                logger.info(f"⏳ Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
                
        except requests.exceptions.ConnectionError:
            last_error = {
                "error": "Ollama unreachable",
                "message": f"Could not connect to Ollama at {base_url}. Is it running?"
            }
            logger.error(f"❌ Cannot connect to Ollama - not retrying")
            break  # Don't retry connection errors
            
        except Exception as e:
            last_error = {
                "error": "Ollama error",
                "message": f"Error communicating with Ollama: {str(e)}"
            }
            logger.error(f"❌ Unexpected error: {str(e)}")
            if attempt < max_retries:
                time.sleep(attempt * 5)
    
    # All retries failed
    logger.error(f"❌ All {max_retries} attempts failed")
    if last_error:
        last_error["attempts"] = max_retries
    return last_error or {"error": "Unknown error", "message": "All retry attempts failed"}



def get_career_recommendations(user_input: dict, use_mock: bool = False) -> dict:
    """
    Main function to get career recommendations - REAL AI ONLY, NO MOCKS
    """
    logger.info(f"🚀 Starting recommendation request for user: {user_input.get('name', 'Unknown')}")
    
    # Check environment variable for demo mode
    if os.getenv('USE_MOCK_AI', 'false').lower() == 'true':
        use_mock = True
        logger.info("📌 Mock mode enabled via USE_MOCK_AI environment variable")
    
    # Check cache first to avoid duplicate API calls
    cache_key = _get_cache_key(user_input)
    if cache_key in _response_cache:
        cached_data, cache_time = _response_cache[cache_key]
        if time.time() - cache_time < _cache_timeout:
            logger.info(f"✅ Cache HIT - Returning cached response (saved API quota!)")
            return cached_data
    logger.debug(f"❌ Cache MISS - Will call AI provider")
    
    disclaimer = (
        "These are AI-generated suggestions based on Delhi market data and your profile. "
        "This tool does not make career decisions for you. Please reflect on these options, "
        "do your own research, and consult with mentors or career counselors before making "
        "important decisions about your career path."
    )
    
    # If mock mode, use mock data (for demo without API calls)
    if use_mock:
        result = get_mock_recommendations(user_input)
        result["disclaimer"] = disclaimer
        result["demo_mode"] = True
        return result
    
    # Determine provider
    ai_provider = getattr(settings, 'AI_PROVIDER', 'gemini').lower()
    logger.info(f"🎯 Selected AI provider: {ai_provider}")
    
    # Check if AI is available
    if ai_provider == 'gemini' and not GEMINI_AVAILABLE:
        return {
            "error": "AI service unavailable",
            "message": "The Gemini AI package is not installed. Please install google-genai package.",
            "user_name": user_input.get('name', 'User')
        }
        
    if ai_provider == 'ollama':
        ollama_model = getattr(settings, 'OLLAMA_MODEL', 'mistral')
        logger.info(f"🦙 Using Ollama with model: {ollama_model}")
        
        market_data = load_delhi_market_data()
        language = user_input.get('preferred_language', 'english')
        
        # Simplify prompt slightly for Ollama if needed, but standard one works well with decent models
        prompt = build_prompt(user_input, market_data, language)
        logger.debug(f"Prompt length: {len(prompt)} characters")
        
        start_time = time.time()
        result = get_ollama_recommendations(user_input, prompt)
        elapsed = time.time() - start_time
        
        if "error" not in result:
            logger.info(f"✅ Ollama response received in {elapsed:.2f}s")
            result["user_name"] = user_input.get('name', 'User')
            result["preferred_language"] = language
            result["disclaimer"] = disclaimer
            
            # Cache the successful result
            _response_cache[cache_key] = (result, time.time())
            logger.debug("Response cached successfully")
        else:
            logger.error(f"❌ Ollama error after {elapsed:.2f}s: {result.get('error')}")
            
        return result

    # Default to Gemini logic if not ollama
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return {
            "error": "API key missing",
            "message": "Gemini API key is not configured. Please add GEMINI_API_KEY to your environment.",
            "user_name": user_input.get('name', 'User')
        }
    
    try:
        # Create client with API key
        client = genai.Client(api_key=api_key)
        
        # Configuration for generation
        config = genai.types.GenerateContentConfig(
            temperature=0.3,
            #max_output_tokens=8000,
            response_mime_type="application/json",
            safety_settings=[
                genai.types.SafetySetting(
                    category="HARM_CATEGORY_HARASSMENT",
                    threshold="BLOCK_NONE"
                ),
                genai.types.SafetySetting(
                    category="HARM_CATEGORY_HATE_SPEECH",
                    threshold="BLOCK_NONE"
                ),
                genai.types.SafetySetting(
                    category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    threshold="BLOCK_NONE"
                ),
                genai.types.SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_NONE"
                ),
            ]
        )
        
        market_data = load_delhi_market_data()
        language = user_input.get('preferred_language', 'english')
        prompt = build_prompt(user_input, market_data, language)
        
        # Generate content using client
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',  # Available model (verified in test_models.py)
            contents=prompt,
            config=config
        )
        
        # Extract text from response
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        # Check for empty or truncated response
        if not response_text or len(response_text) < 500:
            return {
                "error": "AI response truncated",
                "message": "The AI returned an incomplete response. Please try again.",
                "user_name": user_input.get('name', 'User')
            }
        
        result = parse_ai_response(response_text)
        
        # Validate result
        is_valid, validation_errors = validate_ai_response(result)
        
        if not is_valid:
            error_summary = "; ".join(validation_errors[:3])
            return {
                "error": "AI response validation failed",
                "message": f"The AI response did not meet quality standards: {error_summary}",
                "user_name": user_input.get('name', 'User')
            }
        
        if "recommendations" in result:
            result["user_name"] = user_input.get('name', 'User')
            result["preferred_language"] = language
            result["disclaimer"] = disclaimer
            result["source"] = "gemini-ai"  # Real AI generation
            
            # Cache the successful result
            _response_cache[cache_key] = (result, time.time())
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        
        # Check for specific error types
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            return {
                "error": "API quota exceeded",
                "message": "The AI service has reached its usage limit. Please try again later or upgrade your API plan.",
                "user_name": user_input.get('name', 'User'),
                "retry_after": "Please wait a few minutes and try again"
            }
        elif "503" in error_msg or "UNAVAILABLE" in error_msg:
            return {
                "error": "AI service overloaded",
                "message": "The AI model is currently experiencing high traffic. Please try again in a few moments.",
                "user_name": user_input.get('name', 'User'),
                "retry_after": "Retry in 30-60 seconds"
            }
        elif "404" in error_msg or "NOT_FOUND" in error_msg:
            return {
                "error": "Model not found",
                "message": "The requested AI model is not available. Please contact support.",
                "user_name": user_input.get('name', 'User')
            }
        else:
            return {
                "error": "AI service error",
                "message": f"An unexpected error occurred: {error_msg[:200]}",
                "user_name": user_input.get('name', 'User')
            }


def get_mock_recommendations(user_input: dict) -> dict:
    """
    Mock function for testing without API key
    Returns dynamic recommendations based on user input including:
    - Financial constraints
    - Time availability
    - Course/stream
    - Covered skills
    - Career interests
    """
    # Extract user inputs
    name = user_input.get('name', 'User')
    course_stream = user_input.get('course_stream', '').lower()
    covered_skills = user_input.get('covered_skills', '').lower()
    career_inclination = user_input.get('career_inclination', '').lower()
    time_availability = user_input.get('time_availability', '').lower()
    financial_constraint = user_input.get('financial_constraint', False)
    preferred_language = user_input.get('preferred_language', 'english')
    
    # Define possible career pathways with metadata
    pathways = {
        "software_developer": {
            "pathway_name": "Software Developer",
            "description": "Design, develop, and maintain software applications using modern technologies in Delhi NCR's thriving IT sector.",
            "required_skills": ["Python", "JavaScript", "SQL", "Git", "Problem Solving"],
            "estimated_salary": "₹6-15 LPA",
            "estimated_salary_budget": "₹4-8 LPA (entry-level, startups)",
            "growth_prospects": "Excellent - Delhi NCR has 50,000+ IT companies including Google, Microsoft, Amazon offices",
            "time_commitment": "high",
            "training_cost": "low",
            "keywords": ["programming", "coding", "software", "tech", "it", "computer", "development", "python", "java", "web"]
        },
        "data_analyst": {
            "pathway_name": "Data Analyst",
            "description": "Analyze data sets and create insights to help businesses make informed decisions, particularly in Delhi's finance and tech sectors.",
            "required_skills": ["Excel", "SQL", "Python", "Data Visualization", "Statistics"],
            "estimated_salary": "₹5-12 LPA",
            "estimated_salary_budget": "₹3-7 LPA (entry-level)",
            "growth_prospects": "Very Good - Data-driven decisions are priority for all businesses",
            "time_commitment": "medium",
            "training_cost": "low",
            "keywords": ["data", "analytics", "statistics", "excel", "numbers", "analysis", "insights", "business"]
        },
        "digital_marketing": {
            "pathway_name": "Digital Marketing Specialist",
            "description": "Plan and execute digital marketing campaigns across various online platforms to help businesses reach their target audience.",
            "required_skills": ["SEO", "Google Ads", "Social Media", "Content Writing", "Analytics"],
            "estimated_salary": "₹4-10 LPA",
            "estimated_salary_budget": "₹3-6 LPA (entry-level)",
            "growth_prospects": "Good - Digital transformation is accelerating across industries",
            "time_commitment": "medium",
            "training_cost": "very_low",
            "keywords": ["marketing", "social media", "seo", "content", "creative", "advertising", "campaigns", "communication"]
        },
        "ui_ux_designer": {
            "pathway_name": "UI/UX Designer",
            "description": "Create intuitive and visually appealing user interfaces and experiences for digital products and services.",
            "required_skills": ["Figma", "Adobe XD", "User Research", "Prototyping", "Design Thinking"],
            "estimated_salary": "₹5-12 LPA",
            "estimated_salary_budget": "₹3-7 LPA (entry-level)",
            "growth_prospects": "Excellent - Every digital product needs good design",
            "time_commitment": "medium",
            "training_cost": "low",
            "keywords": ["design", "creative", "ui", "ux", "graphics", "visual", "interface", "figma", "adobe"]
        },
        "business_analyst": {
            "pathway_name": "Business Analyst",
            "description": "Bridge the gap between business needs and technology solutions by analyzing processes and recommending improvements.",
            "required_skills": ["Requirements Analysis", "SQL", "Excel", "Communication", "Problem Solving"],
            "estimated_salary": "₹5-13 LPA",
            "estimated_salary_budget": "₹3-8 LPA (entry-level)",
            "growth_prospects": "Very Good - Essential role in all growing companies",
            "time_commitment": "medium",
            "training_cost": "very_low",
            "keywords": ["business", "analyst", "consulting", "management", "strategy", "process", "bba", "mba", "commerce"]
        },
        "content_writer": {
            "pathway_name": "Content Writer/Creator",
            "description": "Create engaging written content for websites, blogs, social media, and marketing materials.",
            "required_skills": ["Writing", "SEO", "Research", "Grammar", "Creativity"],
            "estimated_salary": "₹3-8 LPA",
            "estimated_salary_budget": "₹2-5 LPA (entry-level)",
            "growth_prospects": "Good - Content is key for digital presence",
            "time_commitment": "flexible",
            "training_cost": "very_low",
            "keywords": ["writing", "content", "creative", "communication", "english", "journalism", "media", "blogging"]
        },
        "graphic_designer": {
            "pathway_name": "Graphic Designer",
            "description": "Create visual concepts and designs for various media including digital and print.",
            "required_skills": ["Adobe Photoshop", "Illustrator", "Creativity", "Typography", "Color Theory"],
            "estimated_salary": "₹3-9 LPA",
            "estimated_salary_budget": "₹2-5 LPA (entry-level, freelance)",
            "growth_prospects": "Good - Visual content in high demand",
            "time_commitment": "flexible",
            "training_cost": "low",
            "keywords": ["design", "graphics", "creative", "visual", "art", "photoshop", "illustrator", "branding"]
        },
        "junior_legal_associate": {
            "pathway_name": "Junior Legal Associate / Litigation Assistant",
            "description": "Assist senior advocates and law firms with legal research, case preparation, drafting petitions, and attending court proceedings.",
            "required_skills": [
                "Legal Research",
                "Drafting & Pleadings",
                "Case Analysis",
                "Court Procedure Knowledge",
                "Communication"
            ],
            "estimated_salary": "₹3-6 LPA",
            "estimated_salary_budget": "₹2-4 LPA (entry-level chambers)",
            "growth_prospects": "Strong long-term growth in Delhi NCR with experience, specialization, and networking",
            "time_commitment": "high",
            "training_cost": "very_low",
            "keywords": [
                "law",
                "litigation",
                "advocate",
                "court",
                "legal associate",
                "pleadings",
                "case law",
                "ba llb",
                "llb"
            ]
        },
        "policy_research_analyst": {
            "pathway_name": "Policy Research & Think Tank Analyst",
            "description": "Research laws, public policies, and social issues for think tanks, NGOs, government-linked institutions, and research organizations.",
            "required_skills": [
                "Policy Analysis",
                "Research Methodology",
                "Legal Writing",
                "Critical Thinking",
                "Data Interpretation"
            ],
            "estimated_salary": "₹4-7 LPA",
            "estimated_salary_budget": "₹3-5 LPA (research roles, NGOs)",
            "growth_prospects": "Steady growth with specialization in public policy, governance, or regulatory affairs",
            "time_commitment": "medium",
            "training_cost": "low",
            "keywords": [
                "policy",
                "research",
                "think tank",
                "public policy",
                "governance",
                "law",
                "analysis",
                "ba llb",
                "llb",
                "ngo"
            ]
        },
        "digital_marketer": {
            "pathway_name": "Digital Marketer",
            "description": "Manage online marketing campaigns, SEO, social media, and email marketing.",
            "required_skills": ["SEO", "Social Media", "Analytics", "Content Marketing", "Email Marketing"],
            "estimated_salary": "₹3-8 LPA",
            "estimated_salary_budget": "₹2-5 LPA (entry-level)",
            "growth_prospects": "Good - Digital marketing is always in demand",
            "time_commitment": "flexible",
            "training_cost": "very_low",
            "keywords": ["marketing", "digital", "online", "social media", "seo", "analytics", "content marketing", "email marketing"]
        },
        "content_writer": {
            "pathway_name": "Content Writer",
            "description": "Create engaging and informative content for websites, blogs, social media, and marketing materials.",
            "required_skills": ["Writing", "SEO", "Content Strategy", "Editing", "Research"],
            "estimated_salary": "₹3-8 LPA",
            "estimated_salary_budget": "₹2-5 LPA (entry-level)",
            "growth_prospects": "Good - Content is always in demand",
            "time_commitment": "flexible",
            "training_cost": "very_low",
            "keywords": ["writing", "content", "creative", "communication", "english", "journalism", "media", "blogging"]
        },
        "social_media_manager": {
            "pathway_name": "Social Media Manager",
            "description": "Manage social media accounts, create content, and engage with followers.",
            "required_skills": ["Social Media", "Content Creation", "Analytics", "Engagement", "Content Strategy"],
            "estimated_salary": "₹3-8 LPA",
            "estimated_salary_budget": "₹2-5 LPA (entry-level)",
            "growth_prospects": "Good - Social media is always in demand",
            "time_commitment": "flexible",
            "training_cost": "very_low",
            "keywords": ["social media", "management", "engagement", "content", "analytics", "strategy", "marketing", "digital"]
        },
        "legal_content_compliance": {
            "pathway_name": "Legal Content & Compliance Specialist",
            "description": "Work on drafting legal documents, compliance policies, contracts, and regulatory content for corporates, startups, and legal-tech companies.",
            "required_skills": [
                "Legal Research",
                "Legal Drafting",
                "Compliance Knowledge",
                "Attention to Detail",
                "Written Communication"
            ],
            "estimated_salary": "₹4-8 LPA",
            "estimated_salary_budget": "₹3-6 LPA (entry-level, corporates/startups)",
            "growth_prospects": "Good - Increasing demand in Delhi NCR due to startup growth, compliance needs, and legal-tech expansion",
            "time_commitment": "medium",
            "training_cost": "very_low",
            "keywords": [
                "law",
                "legal",
                "compliance",
                "contracts",
                "corporate law",
                "documentation",
                "policy",
                "ba llb",
                "llb",
                "non-tech"
            ]
        },
        "junior_legal_associate": {
            "pathway_name": "Junior Legal Associate / Litigation Assistant",
            "description": "Assist senior advocates and law firms with legal research, case preparation, drafting petitions, and attending court proceedings.",
            "required_skills": [
                "Legal Research",
                "Drafting & Pleadings",
                "Case Analysis",
                "Court Procedure Knowledge",
                "Communication"
            ],
            "estimated_salary": "₹3-6 LPA",
            "estimated_salary_budget": "₹2-4 LPA (entry-level chambers)",
            "growth_prospects": "Strong long-term growth in Delhi NCR with experience, specialization, and networking",
            "time_commitment": "high",
            "training_cost": "very_low",
            "keywords": [
                "law",
                "litigation",
                "advocate",
                "court",
                "legal associate",
                "pleadings",
                "case law",
                "ba llb",
                "llb"
            ]
        },
        "policy_research_analyst": {
            "pathway_name": "Policy Research & Think Tank Analyst",
            "description": "Research laws, public policies, and social issues for think tanks, NGOs, government-linked institutions, and research organizations.",
            "required_skills": [
                "Policy Analysis",
                "Research Methodology",
                "Legal Writing",
                "Critical Thinking",
                "Data Interpretation"
            ],
            "estimated_salary": "₹4-7 LPA",
            "estimated_salary_budget": "₹3-5 LPA (research roles, NGOs)",
            "growth_prospects": "Steady growth with specialization in public policy, governance, or regulatory affairs",
            "time_commitment": "medium",
            "training_cost": "low",
            "keywords": [
                "policy",
                "research",
                "think tank",
                "public policy",
                "governance",
                "law",
                "analysis",
                "ba llb",
                "llb",
                "ngo"
            ]
        }
    }
    # Score each pathway based on user input
    pathway_scores = {}
    for key, pathway in pathways.items():
        score = 0
        
        # Match against career inclination and course
        combined_text = f"{course_stream} {covered_skills} {career_inclination}"
        for keyword in pathway["keywords"]:
            if keyword in combined_text:
                score += 2
        
        # Bonus for financial constraints - prefer lower training cost
        if financial_constraint:
            if pathway["training_cost"] == "very_low":
                score += 3
            elif pathway["training_cost"] == "low":
                score += 1
        
        # Bonus for time availability
        if "part" in time_availability or "limited" in time_availability or "few" in time_availability:
            if pathway["time_commitment"] == "flexible":
                score += 3
            elif pathway["time_commitment"] == "medium":
                score += 1
        elif "full" in time_availability:
            if pathway["time_commitment"] == "high":
                score += 2
        
        pathway_scores[key] = score
    
    # Get top 3 pathways
    top_pathways = sorted(pathway_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # If all scores are 0 (no matches), use default recommendations
    if top_pathways[0][1] == 0:
        top_pathways = [("software_developer", 0), ("data_analyst", 0), ("digital_marketing", 0)]
    
    # Build recommendations
    recommendations = []
    fit_scores = ["Strong fit", "Moderate fit", "Worth exploring"]
    
    for rank, (pathway_key, score) in enumerate(top_pathways, 1):
        pathway = pathways[pathway_key]
        
        # Build personalized "why_recommended" text IN MENTORING TONE
        why_parts = []
        
        # Start conversational
        opening = f"Look, {name}, " if name != "User" else "Look, "
        
        # Reference their course/stream
        if course_stream:
            why_parts.append(f"with your {course_stream} background")
        
        # Reference their skills THEY already have
        if covered_skills:
            skills_mentioned = []
            for skill in pathway["required_skills"]:
                if skill.lower() in covered_skills:
                    skills_mentioned.append(skill)
            
            if skills_mentioned:
                why_parts.append(f"and those {', '.join(skills_mentioned)} skills YOU already have")
        
        # Reference THEIR career interests
        if career_inclination:
            why_parts.append(f"plus YOUR interest in {career_inclination}")
        
        # Build the recommendation in FIRST PERSON
        if why_parts:
            why_recommended = f"{opening}{', '.join(why_parts)}, I think this could be a really solid path for you. "
        else:
            why_recommended = f"{opening}I genuinely think this pathway could work well for you. "
        
        # Add specific Delhi context
        why_recommended += f"Delhi NCR has tons of opportunities in this space."
        
        # Add time/budget context PERSONALLY
        if time_availability:
            if pathway["time_commitment"] == "flexible" and ("part" in time_availability.lower() or "limited" in time_availability.lower()):
                why_recommended += f" Plus, the flexible nature of this work fits perfectly with your schedule."
            elif pathway["time_commitment"] == "high" and "full" in time_availability.lower():
                why_recommended += f" And since you can dedicate full-time to this, you'll be able to dive deep and really master it."

        
        # Build considerations based on financial constraints IN MENTORING TONE
        considerations = [
            "You'll need to keep learning continuously - this field evolves fast",
            "Building real experience will take 3-6 months, but that's totally normal"
        ]
        
        if financial_constraint:
            if pathway["training_cost"] == "very_low":
                considerations.append("Great news for your budget - tons of free resources available online!")
            elif pathway["training_cost"] == "low":
                considerations.append("Budget-friendly path - free resources exist, though some affordable courses can help")
            else:
                considerations.append("Heads up - you might need to budget for some paid courses or certifications")
        else:
            considerations.append("I'd suggest investing in some quality courses - it'll speed up your growth significantly")
        
        # Build next steps based on financial constraints IN FIRST PERSON
        next_steps = []
        if financial_constraint:
            next_steps.append("Start with free resources - YouTube, freeCodeCamp, Google certifications are gold")
            next_steps.append("Build a portfolio using free tools to showcase what you can do")
            next_steps.append("Get active on LinkedIn and join free community groups - networking is key")
            if time_availability and "full" in time_availability.lower():
                next_steps.append("Apply for internships or entry-level roles - you'll learn on the job")
            else:
                next_steps.append("Check out freelance projects on Fiverr or Upwork to build experience")
        else:
            next_steps.append("Enroll in a solid certification program - it's worth the investment")
            next_steps.append("Build a strong portfolio with 3-5 quality projects that show your skills")
            next_steps.append("Network with professionals and hit up industry events - connections matter")
            next_steps.append("Apply for positions that offer good mentorship and growth opportunities")

        
        # Choose salary range based on financial constraint
        salary = pathway["estimated_salary_budget"] if financial_constraint else pathway["estimated_salary"]
        
        recommendations.append({
            "rank": rank,
            "pathway_name": pathway["pathway_name"],
            "description": pathway["description"],
            "why_recommended": why_recommended,
            "fit_score": fit_scores[rank - 1],
            "required_skills": pathway["required_skills"],
            "estimated_salary": salary,
            "growth_prospects": pathway["growth_prospects"],
            "considerations": considerations,
            "next_steps": next_steps
        })
    
    return {
        "user_name": name,
        "preferred_language": preferred_language,
        "recommendations": recommendations,
        "source": "mock-fallback"  # Indicates mock data, not real AI
    }
