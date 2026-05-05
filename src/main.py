#!/usr/bin/env python3
"""Main CLI interface for Kali AI Assistant"""

import os
import sys
import argparse
import logging
from typing import Optional
from colorama import Fore, Style

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from groq_integration import GroqClient
from cache_manager import CacheManager
from voice_handler import VoiceHandler
from utils import (
    setup_logging, print_header, print_success, print_error,
    print_info, print_response, print_warning, get_user_input,
    validate_api_key, load_env_file, clear_screen
)

logger = logging.getLogger(__name__)

class KaliAIAssistant:
    """Main Kali AI Assistant class"""
    
    def __init__(self, use_voice: bool = False, debug: bool = False):
        """Initialize the assistant"""
        # Setup logging
        setup_logging(debug)
        
        # Load environment variables
        load_env_file()
        
        # Validate API key
        api_key = os.getenv("GROQ_API_KEY")
        if not validate_api_key(api_key):
            print_error("Groq API key not found or invalid!")
            print_info("Please set GROQ_API_KEY in .env file or environment variable")
            print_info("Get your free API key at: https://console.groq.com")
            sys.exit(1)
        
        # Initialize components
        self.groq_client = GroqClient(api_key)
        self.cache_manager = CacheManager()
        self.voice_handler = VoiceHandler(enabled=use_voice)
        self.running = True
        self.debug = debug
        
        logger.info("Kali AI Assistant initialized")
    
    def display_help(self):
        """Display help message"""
        help_text = f"""
{Fore.CYAN}{Style.BRIGHT}Available Commands:{Style.RESET_ALL}

  /help          - Show this help message
  /voice         - Toggle voice input/output
  /clear         - Clear conversation history
  /cache-stats   - Show cache statistics
  /cache-clear   - Clear all cached queries
  /exit, /quit   - Exit the assistant
  /listen        - Listen for voice input (microphone)
  /speak TEXT    - Speak text using TTS

{Fore.CYAN}{Style.BRIGHT}Quick Examples:{Style.RESET_ALL}

  > What is SQL injection?
  > How do I scan for open ports with nmap?
  > Explain the three-way handshake in TCP
  > How do I set up a reverse shell?

{Fore.CYAN}{Style.BRIGHT}Features:{Style.RESET_ALL}

  ✓ Smart caching for repeated queries
  ✓ Voice input/output support
  ✓ Conversation history
  ✓ Groq's fast inference models
  ✓ Kali Linux-optimized prompts
        """
        print(help_text)
    
    def handle_command(self, user_input: str) -> bool:
        """Handle special commands"""
        command = user_input.lower().strip()
        
        if command in ["/exit", "/quit"]:
            print_success("Goodbye! Stay ethical and stay safe.")
            return False
        
        elif command == "/help":
            self.display_help()
            return True
        
        elif command == "/voice":
            self.voice_handler.toggle_voice()
            return True
        
        elif command == "/clear":
            self.groq_client.clear_history()
            print_success("Conversation history cleared")
            return True
        
        elif command == "/cache-stats":
            stats = self.cache_manager.get_stats()
            if stats:
                print_response("Cache Statistics", f"""
Total Cached Queries: {stats['total_cached_queries']}
Total Cache Hits: {stats['total_cache_hits']}
Average Hits per Query: {stats['average_hits_per_query']}
                """)
            else:
                print_info("Cache is disabled or empty")
            return True
        
        elif command == "/cache-clear":
            if self.cache_manager.clear():
                print_success("Cache cleared")
            else:
                print_error("Failed to clear cache")
            return True
        
        elif command == "/listen":
            print_info("Listening for voice input...")
            text = self.voice_handler.listen()
            if text:
                print_success(f"Heard: {text}")
                return self.process_query(text)
            return True
        
        elif command.startswith("/speak"):
            text = command.replace("/speak", "").strip()
            if text:
                self.voice_handler.speak(text)
                print_success(f"Spoke: {text}")
            return True
        
        return None  # Not a command
    
    def process_query(self, user_input: str) -> bool:
        """Process user query and get response"""
        if not user_input:
            return True
        
        try:
            # Check cache first
            cached_response = self.cache_manager.get(user_input)
            
            if cached_response:
                print_response("KALI (Cached)", cached_response)
                self.voice_handler.speak(cached_response[:500])  # Speak first 500 chars
                return True
            
            # Get new response from Groq
            print_info("Processing your query...")
            
            # Use streaming for better UX
            print(f"{Fore.GREEN}[KALI] {Style.RESET_ALL}", end="", flush=True)
            
            full_response = ""
            for chunk in self.groq_client.get_streaming_response(user_input):
                print(chunk, end="", flush=True)
                full_response += chunk
            
            print("\n")  # New line after streaming
            
            # Cache the response
            self.cache_manager.set(user_input, full_response)
            
            # Speak the response (first 500 chars)
            self.voice_handler.speak(full_response[:500])
            
            return True
            
        except Exception as e:
            print_error(f"Error processing query: {str(e)}")
            if self.debug:
                logger.exception("Full error trace:")
            return True
    
    def run(self):
        """Main interactive loop"""
        clear_screen()
        print_header()
        
        print_success(f"Welcome! Groq Model: {self.groq_client.model}")
        print_info("Type '/help' for available commands")
        print_info(f"Voice: {'Enabled 🔊' if self.voice_handler.enabled else 'Disabled 🔇'}")
        print()
        
        while self.running:
            try:
                user_input = get_user_input("kali> ")
                
                if not user_input:
                    continue
                
                # Check if it's a command
                if user_input.startswith("/"):
                    result = self.handle_command(user_input)
                    if result is False:
                        self.running = False
                    continue
                
                # Process as query
                self.process_query(user_input)
                
            except KeyboardInterrupt:
                print()
                print_warning("Interrupted by user")
                confirm = get_user_input("Exit? (y/n): ").lower()
                if confirm == 'y':
                    self.running = False
            except Exception as e:
                print_error(f"Unexpected error: {str(e)}")
                if self.debug:
                    logger.exception("Full error trace:")

def main():
    """Entry point for the application"""
    parser = argparse.ArgumentParser(
        description="Kali AI Assistant - AI-powered assistant for Kali Linux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kali-ai                          # Start interactive mode
  kali-ai --voice                  # Enable voice input/output
  kali-ai --debug                  # Enable debug logging
  kali-ai --query "What is nmap?" # Single query mode
        """
    )
    
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Enable voice input/output"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--query",
        type=str,
        help="Single query mode (non-interactive)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="mixtral-8x7b-32768",
        help="Groq model to use (default: mixtral-8x7b-32768)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Kali AI Assistant 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Set model if provided
    if args.model:
        os.environ["MODEL"] = args.model
    
    # Initialize assistant
    assistant = KaliAIAssistant(use_voice=args.voice, debug=args.debug)
    
    # Single query mode
    if args.query:
        assistant.process_query(args.query)
    else:
        # Interactive mode
        assistant.run()

if __name__ == "__main__":
    main()
