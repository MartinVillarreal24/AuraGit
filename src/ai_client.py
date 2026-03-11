import requests
import json
import os
from abc import ABC, abstractmethod
from typing import Optional
from config import Config

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_commit_message(self, diff: str, context: str = "") -> str:
        pass

    @abstractmethod
    def check_connection(self) -> bool:
        pass

class OllamaProvider(BaseAIProvider):
    def __init__(self):
        self.url = f"{Config.OLLAMA_URL}/api/generate"
        self.model = Config.OLLAMA_MODEL

    def generate_commit_message(self, diff: str, context: str = "") -> str:
        prompt = self._get_prompt(diff, context)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        }
        try:
            response = requests.post(self.url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"Ollama Error: {str(e)}"

    def check_connection(self) -> bool:
        try:
            response = requests.get(Config.OLLAMA_URL, timeout=5)
            return response.status_code == 200
        except:
            return False

    def _get_prompt(self, diff, context):
        return f"""Professional software engineer. Generate a git commit message using Conventional Commits.
Context: {context}
Diff: {diff}
Return ONLY the commit message."""

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL

    def generate_commit_message(self, diff: str, context: str = "") -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional software engineer."},
                    {"role": "user", "content": f"Generate a Conventional Commit message for this diff:\n\n{diff}"}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI Error: {str(e)}"

    def check_connection(self) -> bool:
        return bool(Config.OPENAI_API_KEY)

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def generate_commit_message(self, diff: str, context: str = "") -> str:
        try:
            response = self.model.generate_content(
                f"Professional software engineer. Generate a Conventional Commit message for this diff. Return ONLY the message.\n\nDiff:\n{diff}"
            )
            return response.text.strip()
        except Exception as e:
            return f"Gemini Error: {str(e)}"

    def check_connection(self) -> bool:
        return bool(Config.GEMINI_API_KEY)

class AnthropicProvider(BaseAIProvider):
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.ANTHROPIC_MODEL

    def generate_commit_message(self, diff: str, context: str = "") -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": f"Professional software engineer. Generate a Conventional Commit message for this diff. Return ONLY the message.\n\nDiff:\n{diff}"}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            return f"Anthropic Error: {str(e)}"

    def check_connection(self) -> bool:
        return bool(Config.ANTHROPIC_API_KEY)

class AIClientFactory:
    @staticmethod
    def get_provider() -> BaseAIProvider:
        provider_name = Config.AI_PROVIDER
        if provider_name == "ollama":
            return OllamaProvider()
        elif provider_name == "openai":
            return OpenAIProvider()
        elif provider_name == "gemini":
            return GeminiProvider()
        elif provider_name == "anthropic":
            return AnthropicProvider()
        else:
            raise ValueError(f"Unknown AI provider: {provider_name}")
