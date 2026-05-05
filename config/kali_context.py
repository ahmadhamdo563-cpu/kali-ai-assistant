"""Kali Linux context and knowledge base"""

# Security testing categories and knowledge
KALI_CONTEXT = {
    "penetration_testing": {
        "description": "Authorized security testing",
        "keywords": ["penetration test", "pentest", "authorized testing"],
        "tools": ["metasploit", "burp suite", "nessus", "nmap", "hydra"],
    },
    "network_security": {
        "description": "Network analysis and security",
        "keywords": ["network", "packet", "firewall", "IDS", "IPS"],
        "tools": ["wireshark", "tcpdump", "nmap", "netstat", "iptables"],
    },
    "web_security": {
        "description": "Web application security",
        "keywords": ["sql injection", "xss", "csrf", "web", "http"],
        "tools": ["burp suite", "zaproxy", "sqlmap", "nikto"],
    },
    "wireless_security": {
        "description": "Wireless network testing",
        "keywords": ["wifi", "wireless", "802.11", "aircrack"],
        "tools": ["aircrack-ng", "airodump-ng", "aireplay-ng"],
    },
    "forensics": {
        "description": "Digital forensics and investigation",
        "keywords": ["forensics", "investigation", "recovery", "evidence"],
        "tools": ["volatility", "autopsy", "sleuthkit"],
    },
    "system_admin": {
        "description": "Linux system administration",
        "keywords": ["linux", "bash", "system", "admin", "configuration"],
        "tools": ["bash", "systemctl", "iptables", "cron"],
    },
}

# Ethical guidelines
ETHICAL_GUIDELINES = """
Impportant Legal and Ethical Guidelines:

1. AUTHORIZATION: Always obtain written permission before testing any system you don't own
2. SCOPE: Stay within the agreed scope of testing
3. CONFIDENTIALITY: Protect and respect any sensitive information discovered
4. APPLICABLE LAWS: Follow all local and international laws
5. RESPONSIBLE DISCLOSURE: Report vulnerabilities responsibly
6. NO HARM: Do not intentionally damage systems or steal data
7. DOCUMENTATION: Keep detailed records of your activities

Unauthorized access to computer systems is illegal and unethical.
Always use these tools for educational and authorized purposes only.
"""

# Common Kali Linux tools
KALI_TOOLS = {
    "nmap": "Network mapper - discovers hosts and services",
    "metasploit": "Penetration testing framework",
    "burp-suite": "Web application security testing",
    "wireshark": "Network protocol analyzer",
    "hashcat": "Password cracking tool",
    "john": "Password cracker",
    "aircrack-ng": "WiFi security auditing",
    "sqlmap": "SQL injection detection and exploitation",
    "hydra": "Network login cracker",
    "nikto": "Web server scanner",
    "steghide": "Steganography tool",
    "truecrypt": "Encryption software",
}
