from rest_framework import serializers


class UserInputSerializer(serializers.Serializer):
    """Serializer for user career assessment input"""
    
    name = serializers.CharField(max_length=100)
    course_stream = serializers.CharField(max_length=200)
    covered_skills = serializers.CharField()
    career_inclination = serializers.CharField(max_length=200)
    time_availability = serializers.CharField(max_length=100)
    financial_constraint = serializers.BooleanField(default=False)
    preferred_language = serializers.ChoiceField(
        choices=['english', 'hindi'],
        default='english'
    )


class CareerPathwaySerializer(serializers.Serializer):
    """Serializer for career pathway recommendations"""
    
    rank = serializers.IntegerField()
    pathway_name = serializers.CharField()
    description = serializers.CharField()
    required_skills = serializers.ListField(child=serializers.CharField())
    estimated_salary = serializers.CharField()
    growth_prospects = serializers.CharField()
    next_steps = serializers.ListField(child=serializers.CharField())
    
    # Enhanced explanation fields
    why_recommended = serializers.CharField(required=False, allow_blank=True)
    considerations = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Trade-offs or challenges to consider"
    )
    fit_score = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Qualitative fit assessment"
    )


class RecommendationResponseSerializer(serializers.Serializer):
    """Serializer for the complete recommendation response"""
    
    user_name = serializers.CharField()
    preferred_language = serializers.CharField()
    disclaimer = serializers.CharField(
        required=False,
        help_text="Important disclaimer about AI recommendations"
    )
    recommendations = CareerPathwaySerializer(many=True)
