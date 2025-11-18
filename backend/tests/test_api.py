import pytest
import httpx
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import os

# Set test environment
os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"] = "test"

from backend.app.main import app

client = TestClient(app)

class TestHealthEndpoints:
    """Test basic health and root endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct message"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "DataGate API is running"}
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "DataGate API"

class TestFileValidation:
    """Test file validation logic"""
    
    def test_allowed_file_extensions(self):
        """Test that allowed file extensions are properly defined"""
        from backend.app.routes.files import ALLOWED_EXTENSIONS
        
        # Check that common file types are allowed
        assert '.pdf' in ALLOWED_EXTENSIONS
        assert '.jpg' in ALLOWED_EXTENSIONS
        assert '.txt' in ALLOWED_EXTENSIONS
        assert '.zip' in ALLOWED_EXTENSIONS
        
        # Check that dangerous extensions are not allowed
        assert '.exe' not in ALLOWED_EXTENSIONS
        assert '.bat' not in ALLOWED_EXTENSIONS
        assert '.sh' not in ALLOWED_EXTENSIONS
    
    def test_max_file_size(self):
        """Test that max file size is properly defined"""
        from backend.app.routes.files import MAX_FILE_SIZE
        
        # Should be 100MB
        assert MAX_FILE_SIZE == 100 * 1024 * 1024

class TestCORSConfiguration:
    """Test CORS configuration"""
    
    def test_cors_headers(self):
        """Test that CORS headers are properly set"""
        response = client.options("/")
        assert response.status_code == 200
        
        # Check CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_protected_endpoints_require_auth(self):
        """Test that protected endpoints require authentication"""
        # Test files endpoint
        response = client.get("/api/files/my-files")
        assert response.status_code == 403
        
        # Test admin endpoint
        response = client.get("/api/admin/users")
        assert response.status_code == 403
    
    def test_upload_endpoint_requires_auth(self):
        """Test that upload endpoint requires authentication"""
        response = client.post("/api/files/upload")
        assert response.status_code == 403

if __name__ == "__main__":
    pytest.main([__file__])
