#!/usr/bin/env python3
import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('CLOCKIFY_API_KEY')
WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
USER_ID = os.getenv('CLOCKIFY_USER_ID')

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

try:
    # Stop the current timer
    data = {
        "end": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    
    response = requests.patch(
        f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Timer stopped successfully!")
        print(f"   Duration: {result.get('timeInterval', {}).get('duration', 'N/A')}")
        print(f"   Description: {result.get('description', 'N/A')}")
    else:
        print(f"❌ Error stopping timer: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")