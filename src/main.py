#!/usr/bin/env python3
"""Enhanced Main CLI with Learning System, Code Analysis, and System Review"""

import os
import sys
import argparse
import logging
import time
from typing import Optional
from colorama import Fore, Style

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from groq_integration import GroqClient
from cache_manager import CacheManager
from voice_handler import VoiceHandler
from learning_system import LearningSystem
from code_analyzer import CodeAnalyzer
from system_analyzer import SystemAnalyzer
from utils import (
    setup_logging, print_header, print_success, print_error,
    print_info, print_response, print_warning, get_user_input,
    validate_api_key, load_env_file, clear_screen, print_table
)

logger = logging.getLogger(__name__)

class KaliAIAssistant:
    """Enhanced Kali AI Assistant with learning and analysis capabilities"""
    
    def __init__(self, use_voice: bool = False, debug: bool = False):
        """Initialize the enhanced assistant"""
        setup_logging(debug)
        load_env_file()
        
        api_key = os.getenv("GROQ_API_KEY")
        if not validate_api_key(api_key):
            print_error("Groq API key not found or invalid!")
            print_info("Please set GROQ_API_KEY in .env file")
            sys.exit(1)
        
        # Initialize all components
        self.groq_client = GroqClient(api_key)
        self.cache_manager = CacheManager()
        self.voice_handler = VoiceHandler(enabled=use_voice)
        self.learning_system = LearningSystem()
        self.code_analyzer = CodeAnalyzer()
        self.system_analyzer = SystemAnalyzer()
        self.running = True
        self.debug = debug
        
        logger.info("Kali AI Assistant (Enhanced) initialized")
    
    def display_help(self):
        """Display enhanced help message"""
        help_text = f"""
{Fore.CYAN}{Style.BRIGHT}Available Commands:{Style.RESET_ALL}

{Fore.YELLOW}Interactive Commands:{Style.RESET_ALL}
  /help              - Show this help message
  /voice             - Toggle voice input/output
  /clear             - Clear conversation history
  /exit, /quit       - Exit the assistant

{Fore.YELLOW}Learning & Analytics:{Style.RESET_ALL}
  /learning-stats    - Show learning statistics
  /cache-stats       - Show cache statistics
  /cache-clear       - Clear cached queries
  /model-params      - Show current model parameters

{Fore.YELLOW}Code Analysis & Review:{Style.RESET_ALL}
  /analyze FILE      - Analyze a single code file
  /review DIR        - Review all code in directory
  /security LANG     - Security check for language
  /quality FILE      - Detailed quality analysis

{Fore.YELLOW}System Analysis:{Style.RESET_ALL}
  /system-security   - Full system security audit
  /network-analysis  - Analyze network config
  /process-check     - Check running processes
  /file-permissions  - Audit file permissions
  /vulnerabilities   - Check for known CVEs

{Fore.YELLOW}Voice Commands:{Style.RESET_ALL}
  /listen            - Listen for voice input
  /speak TEXT        - Speak text using TTS

{Fore.CYAN}{Style.BRIGHT}Examples:{Style.RESET_ALL}

  > What is XSS vulnerability?
  > /analyze ./myapp.py
  > /review ./src
  > /system-security
  > /learning-stats
        """
        print(help_text)
    
    def handle_command(self, user_input: str) -> bool:
        """Handle special commands"""
        command = user_input.lower().strip()
        
        # Exit commands
        if command in ["/exit", "/quit"]:
            print_success("Goodbye! Stay ethical and secure.")
            return False
        
        # Help
        elif command == "/help":
            self.display_help()
            return True
        
        # Voice commands
        elif command == "/voice":
            self.voice_handler.toggle_voice()
            return True
        
        elif command == "/listen":
            print_info("🎤 Listening for voice input...")
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
        
        # Learning commands
        elif command == "/learning-stats":
            stats = self.learning_system.get_learning_stats()
            if stats:
                print_response("Learning Statistics", self._format_dict(stats))
            return True
        
        elif command == "/cache-stats":
            stats = self.cache_manager.get_stats()
            if stats:
                print_response("Cache Statistics", self._format_dict(stats))
            return True
        
        elif command == "/cache-clear":
            if self.cache_manager.clear():
                print_success("Cache cleared")
            return True
        
        elif command == "/clear":
            self.groq_client.clear_history()
            print_success("Conversation history cleared")
            return True
        
        elif command == "/model-params":
            params = self.learning_system.parameters
            print_response("Current Model Parameters", self._format_dict(params))
            return True
        
        # Code analysis commands
        elif command.startswith("/analyze"):
            file_path = command.replace("/analyze", "").strip()
            if file_path:
                result = self.code_analyzer.analyze_file(file_path)
                print_response(f"Code Analysis: {file_path}", self._format_dict(result))
            return True
        
        elif command.startswith("/review"):
            dir_path = command.replace("/review", "").strip()
            if dir_path:
                result = self.code_analyzer.analyze_directory(dir_path)
                print_response(f"Directory Review: {dir_path}", self._format_dict(result))
            return True
        
        elif command.startswith("/quality"):
            file_path = command.replace("/quality", "").strip()
            if file_path:
                result = self.code_analyzer.analyze_file(file_path)
                quality_info = {
                    'score': result.get('code_quality_score'),
                    'issues': result.get('quality_issues'),
                    'suggestions': result.get('suggestions')
                }
                print_response(f"Code Quality Analysis", self._format_dict(quality_info))
            return True
        
        # System analysis commands
        elif command == "/system-security":
            print_info("Running comprehensive system security audit...")
            result = self.system_analyzer.analyze_system_security()
            print_response("System Security Audit", self._format_dict(result))
            return True
        
        elif command == "/network-analysis":
            analysis = self.system_analyzer._analyze_network()
            print_response("Network Analysis", self._format_dict(analysis))
            return True
        
        elif command == "/process-check":
            analysis = self.system_analyzer._analyze_processes()
            print_response("Process Analysis", self._format_dict(analysis))
            return True
        
        elif command == "/file-permissions":
            analysis = self.system_analyzer._analyze_file_permissions()
            print_response("File Permissions Audit", self._format_dict(analysis))
            return True
        
        elif command == "/vulnerabilities":
            vulns = self.system_analyzer._check_vulnerabilities()
            print_response("Vulnerability Check", self._format_dict({'vulnerabilities': vulns}))
            return True
        
        return None
    
    def process_query(self, user_input: str) -> bool:
        """Process user query with learning"""
        if not user_input:
            return True
        
        try:
            # Check cache
            cached_response = self.cache_manager.get(user_input)
            
            if cached_response:
                print_response("KALI (Cached)", cached_response)
                self.voice_handler.speak(cached_response[:500])
                
                # Still track learning
                self.learning_system.analyze_interaction(
                    user_input, cached_response, 0.9, 0,
                    self.learning_system.get_optimized_parameters()
                )
                return True
            
            # Get response from Groq with streaming
            print_info("Processing your query...")
            print(f"{Fore.GREEN}[KALI] {Style.RESET_ALL}", end="", flush=True)
            
            start_time = time.time()
            full_response = ""
            
            for chunk in self.groq_client.get_streaming_response(user_input):
                print(chunk, end="", flush=True)
                full_response += chunk
            
            response_time = time.time() - start_time
            print("\n")  # New line
            
            # Cache response
            self.cache_manager.set(user_input, full_response)
            
            # Learn from this interaction
            quality_score = self._evaluate_response_quality(full_response)
            query_type = self.learning_system._classify_query(user_input)
            params = self.learning_system.get_optimized_parameters(query_type)
            
            self.learning_system.analyze_interaction(
                user_input, full_response, quality_score, 0,
                params, len(full_response.split()), response_time
            )
            
            # Speak response
            self.voice_handler.speak(full_response[:500])
            
            return True
            
        except Exception as e:
            print_error(f"Error: {str(e)}")
            if self.debug:
                logger.exception("Full error trace:")
            return True
    
    def _evaluate_response_quality(self, response: str) -> float:
        """Evaluate response quality (0-1)"""
        # Simplified quality metric
        if not response:
            return 0.0
        
        length = len(response.split())
        if length < 10:
            return 0.3
        elif length < 50:
            return 0.6
        elif length < 500:
            return 0.85
        else:
            return 0.9
    
    def _format_dict(self, data: dict) -> str:
        """Format dictionary for display"""
        import json
        return json.dumps(data, indent=2, default=str)
    
    def run(self):
        """Main interactive loop"""
        clear_screen()
        print_header()
        
        print_success(f"Enhanced Kali AI Assistant - Model: {self.groq_client.model}")
        print_info("Features: Voice I/O, Learning System, Code Analysis, System Security")
        print_info("Type '/help' for commands")
        print()
        
        while self.running:
            try:
                user_input = get_user_input("kali> ")
                
                if not user_input:
                    continue
                
                if user_input.startswith("/"):
                    result = self.handle_command(user_input)
                    if result is False:
                        self.running = False
                    continue
                
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
    """Entry point"""
    parser = argparse.ArgumentParser(
        description="Enhanced Kali AI Assistant - AI with Learning, Code Analysis & System Security",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kali-ai                              # Start interactive mode
  kali-ai --voice                      # Enable voice
  kali-ai --query "Analyze XSS"       # Single query
  kali-ai --analyze ./app.py          # Analyze code file
  kali-ai --review ./src              # Review directory
  kali-ai --system-security           # System audit
        """
    )
    
    parser.add_argument("--voice", action="store_true", help="Enable voice I/O")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    parser.add_argument("--query", type=str, help="Single query")
    parser.add_argument("--analyze", type=str, help="Analyze code file")
    parser.add_argument("--review", type=str, help="Review code directory")
    parser.add_argument("--system-security", action="store_true", help="System security audit")
    parser.add_argument("--model", type=str, default="mixtral-8x7b-32768", help="Groq model")
    parser.add_argument("--version", action="version", version="Kali AI Assistant 2.0.0")
    
    args = parser.parse_args()
    os.environ["MODEL"] = args.model
    
    assistant = KaliAIAssistant(use_voice=args.voice, debug=args.debug)
    
    # Handle specific modes
    if args.analyze:
        result = assistant.code_analyzer.analyze_file(args.analyze)
        print_response("Code Analysis", assistant._format_dict(result))
    elif args.review:
        result = assistant.code_analyzer.analyze_directory(args.review)
        print_response("Directory Review", assistant._format_dict(result))
    elif args.system_security:
        result = assistant.system_analyzer.analyze_system_security()
        print_response("System Security Audit", assistant._format_dict(result))
    elif args.query:
        assistant.process_query(args.query)
    else:
        assistant.run()

if __name__ == "__main__":
    main()
