from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.simple_test, name='simple-test'),  # Ultra simple test
    path('', views.health_check, name='api-root'),  # Test root
    path('recommend/', views.CareerRecommendationView.as_view(), name='career-recommend'),
    path('health/', views.health_check, name='health-check'),
    path('sample/', views.get_sample_input, name='sample-input'),
]
