from django.db import models


class UserInput(models.Model):
    """Model to store user career assessment inputs"""
    
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('hindi', 'Hindi'),
    ]
    
    name = models.CharField(max_length=100)
    course_stream = models.CharField(max_length=200)
    covered_skills = models.TextField()
    career_inclination = models.CharField(max_length=200)
    time_availability = models.CharField(max_length=100)
    financial_constraint = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='english')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.course_stream}"


class CareerRecommendation(models.Model):
    """Model to store career recommendations"""
    
    user_input = models.ForeignKey(UserInput, on_delete=models.CASCADE, related_name='recommendations')
    pathway_name = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()
    estimated_salary = models.CharField(max_length=100)
    growth_prospects = models.TextField()
    rank = models.IntegerField()  # 1, 2, or 3
    
    # Enhanced explanation fields
    why_recommended = models.TextField(blank=True, help_text="Clear explanation of why this pathway fits the user")
    considerations = models.TextField(blank=True, help_text="Trade-offs, challenges, or important considerations")
    fit_score = models.CharField(max_length=50, blank=True, help_text="Qualitative fit assessment (e.g., 'Strong fit', 'Worth exploring')")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['rank']
    
    def __str__(self):
        return f"{self.pathway_name} (Rank {self.rank})"
