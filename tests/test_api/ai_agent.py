"""
Unit tests for AI Agent endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

class TestAIAgentEndpoints:

    def test_health_check_success(self):
        """Test successful health check"""
        with patch('app.api.v1.endpoints.ai_agent.get_ai_agent') as mock_agent:
            mock_agent.return_value = MagicMock()
            mock_agent.return_value.client = MagicMock()

            response = client.get("/api/v1/ai/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["ai_agent_available"] is True

    def test_health_check_failure(self):
        """Test health check when agent is unavailable"""
        with patch('app.api.v1.endpoints.ai_agent.get_ai_agent') as mock_agent:
            mock_agent.side_effect = Exception("Agent unavailable")

            response = client.get("/api/v1/ai/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"
            assert data["ai_agent_available"] is False

    def test_chat_success(self):
        """Test successful chat request"""
        with patch('app.api.v1.endpoints.ai_agent.get_ai_agent') as mock_agent:
            mock_instance = MagicMock()
            mock_instance.query_agent.return_value = {
                "success": True,
                "responses": ["Hello! How can I help you?"],
                "message_count": 1,
                "original_query": "Hello"
            }
            mock_agent.return_value = mock_instance

            response = client.post(
                "/api/v1/ai/chat",
                json={"message": "Hello", "include_retrieval": True}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert len(data["responses"]) == 1
            assert data["responses"][0] == "Hello! How can I help you?"

    def test_chat_invalid_input(self):
        """Test chat with invalid input"""
        response = client.post(
            "/api/v1/ai/chat",
            json={"message": "", "include_retrieval": True}
        )

        assert response.status_code == 422  # Validation error

    def test_chat_agent_error(self):
        """Test chat when agent returns error"""
        with patch('app.api.v1.endpoints.ai_agent.get_ai_agent') as mock_agent:
            mock_instance = MagicMock()
            mock_instance.query_agent.return_value = {
                "success": False,
                "error": "Agent processing error"
            }
            mock_agent.return_value = mock_instance

            response = client.post(
                "/api/v1/ai/chat",
                json={"message": "Hello", "include_retrieval": True}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is False
            assert data["error"] == "Agent processing error"
