#!/usr/bin/env python3
"""Simple test script for the API server."""

import requests
import json

API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_chat():
    """Test chat endpoint."""
    print("Testing /chat endpoint...")
    
    # First message
    response = requests.post(
        f"{API_URL}/chat",
        json={"message": "Hello! What is Python?"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response'][:100]}...")
        print(f"Session ID: {data['session_id']}")
        session_id = data['session_id']
        
        # Second message with same session
        print("\nSending follow-up message...")
        response2 = requests.post(
            f"{API_URL}/chat",
            json={
                "message": "Can you tell me more?",
                "session_id": session_id
            }
        )
        
        if response2.status_code == 200:
            data2 = response2.json()
            print(f"Response: {data2['response'][:100]}...")
            print(f"Message count: {data2['message_count']}")
            return True
    
    print(f"Error: {response.status_code} - {response.text}")
    return False

def test_conversation(session_id):
    """Test getting conversation history."""
    print(f"\nTesting /conversations/{session_id} endpoint...")
    response = requests.get(f"{API_URL}/conversations/{session_id}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Session ID: {data['session_id']}")
        print(f"Message count: {data['message_count']}")
        print(f"Messages: {len(data['messages'])}")
        return True
    
    print(f"Error: {response.status_code}")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Chatbruti API Test")
    print("=" * 60)
    print("\nMake sure the API server is running:")
    print("  python -m chatbruti.api_server\n")
    
    try:
        # Test health
        if not test_health():
            print("Health check failed. Is the server running?")
            exit(1)
        
        # Test chat
        if test_chat():
            print("\n✅ Chat test passed!")
        else:
            print("\n❌ Chat test failed!")
            exit(1)
        
        print("\n" + "=" * 60)
        print("All tests passed! ✅")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API server.")
        print("Make sure the server is running:")
        print("  python -m chatbruti.api_server")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)

