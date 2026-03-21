from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InterviewTranscriptViewSet,
    InsightAnalysisViewSet,
    AnalysisTemplateViewSet,
    AnalysisLogViewSet,
    CustomerInsightViewSet
)

router = DefaultRouter()
router.register(r'transcripts', InterviewTranscriptViewSet)
router.register(r'analysis', InsightAnalysisViewSet)
router.register(r'templates', AnalysisTemplateViewSet)
router.register(r'logs', AnalysisLogViewSet)
router.register(r'customer-insights', CustomerInsightViewSet, basename='customer-insights')

urlpatterns = [
    path('', include(router.urls)),
]