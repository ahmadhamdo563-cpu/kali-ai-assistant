# 🐲 Kali AI Assistant

**AI-powered smart assistant for Kali Linux using Groq's fastest inference models**

![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

## Features

✨ **Core Features:**
- 🚀 Lightning-fast responses using Groq API
- 🎤 Voice input/output support
- 💾 Intelligent query caching system
- 🧠 Conversation history management
- 🔐 Security and ethical hacking focused
- 🛠️ Kali Linux optimized
- ⚡ Streaming responses for real-time interaction
- 🎯 Multi-purpose assistant (security, sysadmin, general IT)

## Quick Start

### Prerequisites

- Python 3.8+
- Groq API Key (free at https://console.groq.com)
- Microphone (optional, for voice features)

### Installation

#### Automated Installation (Kali Linux)

```bash
git clone https://github.com/ahmadhamdo563-cpu/kali-ai-assistant.git
cd kali-ai-assistant
chmod +x INSTALL.sh
./INSTALL.sh
```

#### Manual Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ahmadhamdo563-cpu/kali-ai-assistant.git
cd kali-ai-assistant
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure API Key:**
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

5. **Run the assistant:**
```bash
python3 -m src.main
```

## Usage

### Interactive Mode

```bash
# Standard mode
python3 -m src.main

# Enable voice
python3 -m src.main --voice

# Debug mode
python3 -m src.main --debug

# Use different Groq model
python3 -m src.main --model gemma-7b-it
```

### Single Query Mode

```bash
python3 -m src.main --query "What is SQL injection?"
```

### Commands

When in interactive mode, use these commands:

| Command | Description |
|---------|-------------|
| `/help` | Show help message |
| `/voice` | Toggle voice input/output |
| `/clear` | Clear conversation history |
| `/cache-stats` | Show cache statistics |
| `/cache-clear` | Clear all cached queries |
| `/listen` | Listen for voice input |
| `/speak TEXT` | Speak text using TTS |
| `/exit`, `/quit` | Exit the assistant |

### Examples

```bash
kali> What is the difference between TCP and UDP?

kali> How do I use nmap to scan for open ports?

kali> Explain SQL injection vulnerabilities

kali> /voice
🔊 Voice enabled

kali> /cache-stats
[Cache Statistics]
Total Cached Queries: 5
Total Cache Hits: 2
Average Hits per Query: 0.4

kali> /exit
```

## Configuration

Edit `.env` file to customize:

```env
# Groq API Configuration
GROQ_API_KEY=your_api_key_here

# Voice Configuration
VOICE_ENABLED=true
VOICE_LANGUAGE=en-US
VOICE_RATE=150

# Cache Configuration
CACHE_ENABLED=true
CACHE_EXPIRY=86400  # 24 hours

# Assistant Configuration
ASSISTANT_NAME=Kali
DEBUG_MODE=false
MODEL=mixtral-8x7b-32768
```

## Available Models

Groq supports several fast inference models:

- `mixtral-8x7b-32768` ⭐ Recommended (Most capable)
- `llama2-70b-4096`
- `gemma-7b-it`
- `llama-3-70b-8192`
- `llama-3-8b-8192`

## Architecture

```
kali-ai-assistant/
├── src/
│   ├── main.py                 # CLI interface & main loop
│   ├── groq_integration.py     # Groq API client
│   ├── voice_handler.py        # Voice I/O operations
│   ├── cache_manager.py        # Query caching system
│   └── utils.py                # Utility functions
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── .env.example               # Configuration template
├── INSTALL.sh                 # Installation script
└── README.md                  # This file
```

## Features in Detail

### Smart Caching

- Automatically caches frequently asked questions
- Reduces API calls and speeds up responses
- View cache statistics with `/cache-stats`
- Clear cache with `/cache-clear`

### Voice Support

- **Input:** Recognize speech from microphone (Google Speech Recognition)
- **Output:** Text-to-speech responses
- **Toggle:** Enable/disable anytime with `/voice`
- **Language:** Configurable in `.env`

### Conversation History

- Maintains context across queries
- AI remembers previous questions in same session
- Clear history with `/clear` command

### Streaming Responses

- Real-time response streaming for better UX
- See answers as they're generated
- No waiting for full response

## Kali Linux Optimized

Specialized knowledge base includes:

- Penetration testing techniques
- Network security and analysis
- Exploit development
- System administration
- Wireless security
- Social engineering
- Secure coding practices

## Troubleshooting

### "Groq API key not found"

```bash
# Set API key
export GROQ_API_KEY="your_key_here"

# Or create .env file
echo "GROQ_API_KEY=your_key_here" > .env
```

### Voice input not working

```bash
# Install audio dependencies
sudo apt-get install python3-pyaudio

# Or set VOICE_ENABLED=false in .env
```

### Microphone not detected

```bash
# Check available microphones
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_indexes())"
```

### Cache not working

```bash
# Ensure CACHE_ENABLED=true in .env
# Check cache file permissions: ls -la kali_cache.db
```

## Performance

- ⚡ **Response time:** < 2 seconds (average)
- 🚀 **Groq advantage:** 10x faster than traditional LLMs
- 💾 **Cache hit time:** < 100ms
- 🧠 **Context window:** Up to 32k tokens

## Security Notes

⚠️ **Ethical Usage:**
- Use for educational and authorized security testing only
- Always get written permission before penetration testing
- Follow local laws and regulations
- Respect privacy and intellectual property

🔐 **API Security:**
- Never commit `.env` file to git
- Use environment variables for API keys
- Rotate API keys regularly
- Monitor Groq console for unusual activity

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- 🔥 [Groq](https://groq.com) for the lightning-fast inference
- 🐉 [Kali Linux](https://www.kali.org) for the awesome security tools
- 🤖 Community for feedback and contributions

## Support

- 📧 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 🐦 Twitter: [@ahmadhamdo563](https://twitter.com/ahmadhamdo563)

## Roadmap

- [ ] Multi-language support
- [ ] Plugin system for custom commands
- [ ] Web UI interface
- [ ] Docker support
- [ ] Groq Vision integration
- [ ] Custom knowledge base
- [ ] Persistent conversation storage
- [ ] Team collaboration features

---

**Made with ❤️ for the Kali Linux community**

*Remember: Great power comes with great responsibility. Use this tool ethically and legally.*
