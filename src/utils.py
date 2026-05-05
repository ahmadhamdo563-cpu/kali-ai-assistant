"""Utility Functions Module"""

import os
import sys
import logging
from typing import Optional
from colorama import Fore, Back, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def setup_logging(debug: bool = False) -> logging.Logger:
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('kali_assistant.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def print_header():
    """Print ASCII art header"""
    header = f"""
{Fore.RED}{Style.BRIGHT}
╔════════════════════════════════════════════╗
║                                            ║
║      🐲 KALI AI ASSISTANT 🐲               ║
║      Powered by Groq                       ║
║                                            ║
╚════════════════════════════════════════════╝
{Style.RESET_ALL}
    """
    print(header)

def print_success(message: str):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_error(message: str):
    """Print error message"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")

def print_info(message: str):
    """Print info message"""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")

def print_response(title: str, content: str):
    """Print formatted response"""
    print(f"\n{Fore.BLUE}{Style.BRIGHT}[{title}]{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{content}{Style.RESET_ALL}\n")

def get_formatted_timestamp() -> str:
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_table(headers: list, rows: list):
    """Print formatted table"""
    from tabulate import tabulate
    print(tabulate(rows, headers=headers, tablefmt="grid"))

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    return len(api_key) > 0 and api_key != "your_groq_api_key_here"

def load_env_file(env_path: str = ".env") -> bool:
    """Load environment variables from .env file"""
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        return True
    except ImportError:
        print_warning("python-dotenv not installed. Using system environment variables.")
        return False
    except Exception as e:
        print_error(f"Error loading .env file: {str(e)}")
        return False

def get_user_input(prompt: str = "> ") -> str:
    """Get user input with prompt"""
    try:
        return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()
    except KeyboardInterrupt:
        print()
        return ""
    except EOFError:
        return ""
