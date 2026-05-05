from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kali-ai-assistant",
    version="1.0.0",
    author="Ahmad Hamdo",
    description="AI-powered smart assistant for Kali Linux using Groq API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmadhamdo563-cpu/kali-ai-assistant",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Shells",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=[
        "groq>=0.9.0",
        "python-dotenv>=1.0.0",
        "speech-recognition>=3.10.0",
        "pyttsx3>=2.90",
        "requests>=2.31.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "pyyaml>=6.0",
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "kali-ai=src.main:main",
        ],
    },
)
