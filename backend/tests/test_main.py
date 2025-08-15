"""
Tests for the main FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AI Business System Backend"
    assert data["version"] == "1.0.0"


def test_dashboard_metrics():
    """Test dashboard metrics endpoint"""
    response = client.get("/api/v1/dashboard/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "revenue" in data
    assert "expenses" in data
    assert "profit" in data
    assert "roi" in data


def test_dashboard_social_stats():
    """Test social media stats endpoint"""
    response = client.get("/api/v1/dashboard/social-stats")
    assert response.status_code == 200
    data = response.json()
    assert "facebook" in data
    assert "instagram" in data
    assert "twitter" in data
    assert "linkedin" in data


def test_dashboard_ad_performance():
    """Test ad performance endpoint"""
    response = client.get("/api/v1/dashboard/ad-performance")
    assert response.status_code == 200
    data = response.json()
    assert "campaigns" in data
    assert isinstance(data["campaigns"], list)


def test_ai_services_generate_content():
    """Test AI content generation endpoint"""
    response = client.post(
        "/api/v1/ai/generate-content",
        json={
            "topic": "social media marketing",
            "platform": "instagram",
            "tone": "professional"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "suggestions" in data


def test_social_media_posts():
    """Test social media posts endpoint"""
    response = client.get("/api/v1/social-media/posts")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert isinstance(data["posts"], list)


def test_analytics_roi_forecast():
    """Test ROI forecast endpoint"""
    response = client.get("/api/v1/analytics/roi-forecast?days=30")
    assert response.status_code == 200
    data = response.json()
    assert "forecast" in data
    assert "confidence" in data


@pytest.mark.asyncio
async def test_startup_without_credentials():
    """Test that the app starts without external service credentials"""
    # This test verifies that the app can start in development mode
    # without requiring real Supabase or OpenAI credentials
    with TestClient(app) as test_client:
        response = test_client.get("/health")
        assert response.status_code == 200
