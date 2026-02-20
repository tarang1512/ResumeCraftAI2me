"""
Upstox OAuth2 Authentication Module
Handles token generation, refresh, and storage
"""

import os
import time
import base64
import hashlib
import secrets
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlencode, parse_qs, urlparse
from dotenv import load_dotenv

from upstox_bot.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv('/home/ubuntu/.openclaw/workspace/config/.env')


class UpstoxAuth:
    """Handles OAuth2 authentication for Upstox API"""
    
    SANDBOX_BASE_URL = "https://api.sandbox.upstox.com/v2"
    PRODUCTION_BASE_URL = "https://api.upstox.com/v2"
    AUTH_URL = "https://api.upstox.com/v2/login/authorization/dialog"
    TOKEN_URL = "https://api.upstox.com/v2/login/authorization/token"
    
    def __init__(self, api_key: str = None, api_secret: str = None, 
                 redirect_uri: str = None, environment: str = "sandbox"):
        """
        Initialize Upstox authentication
        
        Args:
            api_key: Your Upstox App API Key
            api_secret: Your Upstox App API Secret
            redirect_uri: OAuth2 redirect URI
            environment: "sandbox" or "production"
        """
        self.api_key = api_key or os.getenv("UPSTOX_API_KEY")
        self.api_secret = api_secret or os.getenv("UPSTOX_API_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("UPSTOX_REDIRECT_URI", "http://localhost:8000/callback")
        self.environment = os.getenv("UPSTOX_ENVIRONMENT") or environment or "sandbox"
        
        self.base_url = self.PRODUCTION_BASE_URL if self.environment == "production" else self.SANDBOX_BASE_URL
        
        self.access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
        self.refresh_token = os.getenv("UPSTOX_REFRESH_TOKEN")
        self.token_expiry = None
        
        self._state = None
        self._code_verifier = None
        
        if not self.api_key or not self.api_secret:
            logger.warning("API Key or Secret not provided. Set UPSTOX_API_KEY and UPSTOX_API_SECRET in .env file")
    
    def generate_pkce(self) -> Dict[str, str]:
        """
        Generate PKCE parameters for OAuth2
        
        Returns:
            Dictionary with code_verifier, code_challenge, and state
        """
        # Generate code verifier (43-128 characters)
        self._code_verifier = secrets.token_urlsafe(64)[:128]
        
        # Generate code challenge (SHA256 hash of verifier, base64 encoded)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(self._code_verifier.encode()).digest()
        ).decode().rstrip('=')
        
        # Generate state parameter
        self._state = secrets.token_urlsafe(32)
        
        return {
            "code_verifier": self._code_verifier,
            "code_challenge": code_challenge,
            "state": self._state
        }
    
    def get_authorization_url(self, scope: str = "orders holdings user") -> str:
        """
        Generate OAuth2 authorization URL
        
        Args:
            scope: Space-separated list of permissions
            
        Returns:
            Full authorization URL to redirect user to
        """
        pkce = self.generate_pkce()
        
        params = {
            "client_id": self.api_key,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "state": self._state,
            "scope": scope,
            "code_challenge": pkce["code_challenge"],
            "code_challenge_method": "S256",
            "model": "smart",  # or "web"
        }
        
        auth_url = f"{self.AUTH_URL}?{urlencode(params)}"
        logger.info(f"Generated authorization URL. Visit this URL to authorize:")
        logger.info(auth_url)
        
        return auth_url
    
    def exchange_code_for_token(self, authorization_code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        
        Args:
            authorization_code: Code received from OAuth2 callback
            
        Returns:
            Token response containing access_token, refresh_token, etc.
        """
        if not self._code_verifier:
            raise ValueError("Code verifier not generated. Call get_authorization_url() first.")
        
        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "redirect_uri": self.redirect_uri,
            "code_verifier": self._code_verifier,
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(
                self.TOKEN_URL,
                data=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 3600)
            self.token_expiry = time.time() + expires_in
            
            logger.info("Successfully obtained access token")
            logger.info(f"Token expires in {expires_in} seconds")
            
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to exchange code for token: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """
        Refresh the access token using refresh token
        
        Returns:
            Token response with new tokens
        """
        if not self.refresh_token:
            raise ValueError("No refresh token available. Perform initial authorization.")
        
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(
                self.TOKEN_URL,
                data=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 3600)
            self.token_expiry = time.time() + expires_in
            
            logger.info("Successfully refreshed access token")
            
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to refresh token: {e}")
            raise
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authorization headers for API requests
        Returns:
            Dictionary with Authorization header
        """
        if not self.access_token:
            raise ValueError("No access token available. Authenticate first.")
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def is_token_valid(self) -> bool:
        """Check if current access token is still valid
        Returns:
            True if token exists and hasn't expired
        """
        if not self.access_token:
            return False
        if not self.token_expiry:
            return True  # Assume valid if we don't know expiry
        return time.time() < self.token_expiry - 60  # 60 second buffer
    
    def ensure_valid_token(self):
        """Ensure token is valid, refresh if needed"""
        if not self.is_token_valid():
            if self.refresh_token:
                self.refresh_access_token()
            else:
                raise ValueError("Token expired and no refresh token available")