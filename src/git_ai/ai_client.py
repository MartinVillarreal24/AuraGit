import requests
import json
import os
from abc import ABC, abstractmethod
from typing import Optional
from git_ai.config import Config

class BaseAIProvider(ABC):
    @abstractmethod
    def generate_commit_message(self, diff: str, context: str = "") -> str:
        pass

    @abstractmethod
    def check_connection(self) -> bool:
        pass

    def _get_system_prompt(self) -> str:
        lang = Config.AI_LANGUAGE
        if lang == "es":
            return "Eres un ingeniero de software profesional. Genera un mensaje de commit de git usando la especificación Conventional Commits en ESPAÑOL."
        return "You are a professional software engineer. Generate a git commit message using the Conventional Commits specification in ENGLISH."

    def _get_user_prompt(self, diff: str, context: str = "") -> str:
        lang = Config.AI_LANGUAGE
        if lang == "es":
            return f"""Genera un mensaje de commit profesional en ESPAÑOL para este diff.
Contexto: {context}
Diff:
{diff}

Instrucciones:
1. Usa el formato Conventional Commits (feat:, fix:, etc.).
2. Devuelve ÚNICAMENTE el texto del mensaje de commit.
3. No incluyas explicaciones ni comillas."""
        
        return f"""Generate a professional commit message in ENGLISH for this diff.
Context: {context}
Diff:
{diff}

Instructions:
1. Use the Conventional Commits format (feat:, fix:, etc.).
2. Return ONLY the commit message text.
3. Do not include extra explanations or backticks."""

class OllamaProvider(BaseAIProvider):
    def __init__(self):
        self.url = f"{Config.OLLAMA_URL}/api/generate"
        self.model = Config.OLLAMA_MODEL

    def generate_commit_message(self, diff: str, context: str = "") -> str:
        system = self._get_system_prompt()
        user = self._get_user_prompt(diff, context)
        prompt = f"{system}\n\n{user}"
        
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
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._get_user_prompt(diff, context)}
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
        from google import genai
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model = Config.GEMINI_MODEL

    def generate_commit_message(self, diff: str, context: str = "") -> str:
        try:
            prompt = f"{self._get_system_prompt()}\n\n{self._get_user_prompt(diff, context)}"
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
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
                system=self._get_system_prompt(),
                messages=[
                    {"role": "user", "content": self._get_user_prompt(diff, context)}
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
