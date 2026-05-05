"""Groq API Integration Module"""

import os
from groq import Groq
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GroqClient:
    """Handles all Groq API interactions"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq client with API key"""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Groq API key not found. Please set GROQ_API_KEY environment variable "
                "or pass it as an argument. Get your key at: https://console.groq.com"
            )
        
        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv("MODEL", "mixtral-8x7b-32768")
        self.conversation_history = []
        
    def get_response(self, user_input: str, system_prompt: Optional[str] = None) -> str:
        """Get response from Groq API"""
        try:
            if system_prompt is None:
                system_prompt = self._get_default_system_prompt()
            
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Create messages list with system prompt
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            
            # Get response from Groq
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
                top_p=1,
                stream=False,
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error getting response from Groq: {str(e)}")
            raise
    
    def get_streaming_response(self, user_input: str, system_prompt: Optional[str] = None):
        """Get streaming response from Groq API"""
        try:
            if system_prompt is None:
                system_prompt = self._get_default_system_prompt()
            
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Create messages list
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history)
            
            # Get streaming response
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True,
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Add complete response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
            
        except Exception as e:
            logger.error(f"Error in streaming response: {str(e)}")
            raise
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def _get_default_system_prompt(self) -> str:
        """Get default system prompt for Kali AI Assistant"""
        return """You are Kali, an advanced AI assistant specifically designed for Kali Linux users.
        
Your expertise includes:
- Penetration testing and ethical hacking
- Network security and analysis
- Linux system administration
- Cybersecurity best practices
- Tool usage and configurations
- Vulnerability assessment
- Secure coding practices
- General programming and IT support

You provide detailed, practical answers with examples when relevant.
Always emphasize ethical and legal usage of hacking tools.
When uncertain, ask clarifying questions.
Provide step-by-step guidance when appropriate.

Respond in a friendly, professional manner."""
