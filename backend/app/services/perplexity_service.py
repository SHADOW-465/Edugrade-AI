"""
Service for interacting with the Perplexity API.
"""
import os
import requests
from ...config import get_settings

settings = get_settings()

class PerplexityService:
    """
    Service for interacting with the Perplexity API.
    """
    def __init__(self):
        self.api_key = settings.PERPLEXITY_API_KEY
        self.api_url = "https://api.perplexity.ai/chat/completions"

    def fact_check(self, text):
        """
        Fact-checks a piece of text using the Perplexity API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "pplx-7b-online",
            "messages": [
                {"role": "system", "content": "You are a fact-checker."},
                {"role": "user", "content": f"Is the following statement true or false? '{text}'"},
            ],
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

perplexity_service = PerplexityService()
