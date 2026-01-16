from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserInputSerializer, RecommendationResponseSerializer
from .ai_service import get_career_recommendations
from .models import UserInput, CareerRecommendation


class CareerRecommendationView(APIView):
    """
    API endpoint for career pathway recommendations
    
    POST /api/recommend/
    
    Request Body:
    {
        "name": "User Name",
        "course_stream": "B.Tech Computer Science",
        "covered_skills": "Python, JavaScript, HTML, CSS",
        "career_inclination": "Software Development",
        "time_availability": "Full-time",
        "financial_constraint": false,
        "preferred_language": "english"
    }
    
    Response:
    {
        "user_name": "User Name",
        "preferred_language": "english",
        "disclaimer": "Important disclaimer about AI recommendations...",
        "recommendations": [
            {
                "rank": 1,
                "pathway_name": "...",
                "description": "...",
                "why_recommended": "Clear explanation of fit...",
                "fit_score": "Strong fit",
                "required_skills": [...],
                "estimated_salary": "...",
                "growth_prospects": "...",
                "considerations": ["...", "..."],
                "next_steps": [...]
            },
            ...
        ]
    }
    """
    
    def post(self, request):
        # Validate input
        serializer = UserInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_data = serializer.validated_data
        
        # Save user input to database
        user_input_obj = UserInput.objects.create(
            name=user_data['name'],
            course_stream=user_data['course_stream'],
            covered_skills=user_data['covered_skills'],
            career_inclination=user_data['career_inclination'],
            time_availability=user_data['time_availability'],
            financial_constraint=user_data['financial_constraint'],
            preferred_language=user_data['preferred_language']
        )
        
        # Get AI recommendations
        result = get_career_recommendations(user_data)
        
        # Check for errors and return appropriate status codes
        if "error" in result:
            error_type = result.get("error", "unknown")
            
            # Map error types to HTTP status codes
            if "quota exceeded" in error_type.lower():
                http_status = status.HTTP_429_TOO_MANY_REQUESTS
            elif "unavailable" in error_type.lower() or "overloaded" in error_type.lower():
                http_status = status.HTTP_503_SERVICE_UNAVAILABLE
            elif "not found" in error_type.lower():
                http_status = status.HTTP_404_NOT_FOUND
            elif "api key" in error_type.lower():
                http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            
            # Return FULL error details (not just error field)
            return Response(
                result,  # Return complete error response
                status=http_status
            )
        
        # Save recommendations to database
        if "recommendations" in result:
            for rec in result["recommendations"]:
                # Convert considerations list to comma-separated string for storage
                considerations_str = ', '.join(rec.get('considerations', []))
                
                CareerRecommendation.objects.create(
                    user_input=user_input_obj,
                    pathway_name=rec.get('pathway_name', ''),
                    description=rec.get('description', ''),
                    required_skills=', '.join(rec.get('required_skills', [])),
                    estimated_salary=rec.get('estimated_salary', ''),
                    growth_prospects=rec.get('growth_prospects', ''),
                    rank=rec.get('rank', 0),
                    # New enhanced explanation fields
                    why_recommended=rec.get('why_recommended', ''),
                    considerations=considerations_str,
                    fit_score=rec.get('fit_score', '')
                )
        
        return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def health_check(request):
    """
    Enhanced health check endpoint showing AI provider status.
    
    GET /api/health/
    
    Returns:
        - status: "healthy" or "degraded"
        - provider: active AI provider (ollama/gemini/mock)
        - model: specific model being used
        - ollama_status: connection status if using Ollama
    """
    from django.conf import settings
    import os
    
    # Check if mock mode is enabled
    use_mock = os.getenv('USE_MOCK_AI', 'false').lower() == 'true'
    
    if use_mock:
        return Response({
            "status": "healthy",
            "service": "Delhi Career Navigator API",
            "version": "1.0.0",
            "ai_provider": "mock",
            "ai_model": "mock-fallback",
            "mode": "demo/testing"
        })
    
    # Get provider from settings
    ai_provider = getattr(settings, 'AI_PROVIDER', 'gemini').lower()
    
    if ai_provider == 'ollama':
        ollama_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
        ollama_model = getattr(settings, 'OLLAMA_MODEL', 'mistral')
        
        # Check Ollama connectivity
        try:
            import requests
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                ollama_status = "connected"
                # Check if model is available
                models = response.json().get('models', [])
                model_names = [m.get('name', '') for m in models]
                model_available = ollama_model in model_names or any(ollama_model in m for m in model_names)
            else:
                ollama_status = "error"
                model_available = False
        except:
            ollama_status = "unreachable"
            model_available = False
        
        return Response({
            "status": "healthy" if ollama_status == "connected" else "degraded",
            "service": "Delhi Career Navigator API",
            "version": "1.0.0",
            "ai_provider": "ollama",
            "ai_model": ollama_model,
            "ollama_url": ollama_url,
            "ollama_status": ollama_status,
            "model_available": model_available
        })
    
    else:  # Gemini
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        has_key = bool(api_key and len(api_key) > 10)
        
        return Response({
            "status": "healthy" if has_key else "degraded",
            "service": "Delhi Career Navigator API",
            "version": "1.0.0",
            "ai_provider": "gemini",
            "ai_model": "gemini-2.5-flash",
            "api_key_configured": has_key
        })


@api_view(['GET', 'POST'])
def get_sample_input(request):
    """Returns sample input format for testing"""
    return Response({
        "sample_request": {
            "name": "Rahul Sharma",
            "course_stream": "B.Tech Computer Science",
            "covered_skills": "Python, JavaScript, HTML, CSS, React",
            "career_inclination": "Software Development and AI",
            "time_availability": "Full-time (can dedicate 8+ hours daily)",
            "financial_constraint": False,
            "preferred_language": "english"
        },
        "available_languages": ["english", "hindi"],
        "api_endpoint": "POST /api/recommend/"
    })


@api_view(['GET'])
def simple_test(request):
    """Ultra simple test endpoint"""
    return Response({"status": "working", "message": "Django is running!"})
