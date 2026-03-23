#!/usr/bin/env python3
import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('CLOCKIFY_API_KEY')
WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
PROJECT_ID = os.getenv('CLOCKIFY_PROJECT_ID')

print("🔍 Debug Information:")
print(f"API_KEY: {API_KEY[:10]}... (truncated)")
print(f"WORKSPACE_ID: {WORKSPACE_ID}")
print(f"PROJECT_ID: {PROJECT_ID}")

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "start": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    "description": "Debug test timer",
    "projectId": PROJECT_ID
}

print(f"\n📤 Sending data:")
print(json.dumps(data, indent=2))

try:
    response = requests.post(
        f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/time-entries",
        headers=headers,
        json=data,
        timeout=10
    )
    
    print(f"\n📥 Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"❌ Error: {e}")