#!/usr/bin/env python3
"""Quick test script to verify Groq API key."""

import os
from groq import Groq

# Get API key from environment
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    # Try loading from .env file
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ No GROQ_API_KEY found in environment or .env file")
    exit(1)

print(f"🔑 Testing API key: {api_key[:15]}...")

try:
    client = Groq(api_key=api_key)
    
    # Test with a simple request
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": "Say hello"}],
        max_completion_tokens=10,
    )
    
    print("✅ API key is valid!")
    print(f"Response: {completion.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ API key test failed: {e}")
    print("\n💡 To get a new API key:")
    print("   1. Go to https://console.groq.com/")
    print("   2. Sign in or create an account")
    print("   3. Navigate to API Keys section")
    print("   4. Create a new API key")
    print("   5. Update your .env file with: GROQ_API_KEY=your_new_key")

