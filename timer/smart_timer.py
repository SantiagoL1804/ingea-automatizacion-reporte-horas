#!/usr/bin/env python3
import requests
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def find_latest_timer_by_description(description):
    """Find the most recent timer with matching description"""
    API_KEY = os.getenv('CLOCKIFY_API_KEY')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
    USER_ID = os.getenv('CLOCKIFY_USER_ID')
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # Get recent timers (last 50)
        response = requests.get(
            f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries?page-size=50",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            timers = response.json()
            
            # Find the most recent timer with matching description
            for timer in timers:
                if timer['description'] == description:
                    return timer
        
        return None
        
    except Exception as e:
        print(f"⚠️  Error finding existing timer: {e}")
        return None

def smart_start_timer(description):
    """Smart timer start - continues existing timer or creates new one"""
    API_KEY = os.getenv('CLOCKIFY_API_KEY')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
    PROJECT_ID = os.getenv('CLOCKIFY_PROJECT_ID')
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Check if there's a recent timer with the same description
    existing_timer = find_latest_timer_by_description(description)
    
    if existing_timer:
        # Calculate time since last timer
        last_end = existing_timer['timeInterval']['end']
        if last_end:
            last_end_time = datetime.fromisoformat(last_end.replace('Z', '+00:00'))
            time_diff = datetime.now(timezone.utc) - last_end_time
            hours_since = time_diff.total_seconds() / 3600
            
            if hours_since < 24:  # If less than 24 hours ago
                print(f"🔄 Found recent timer for same task (ended {hours_since:.1f}h ago)")
                print(f"📝 Continuing work on: {description}")
            else:
                print(f"🔄 Found old timer for same task (ended {hours_since:.1f}h ago)")
                print(f"📝 Starting fresh timer for: {description}")
        else:
            print(f"🔄 Found timer for same task (still running?)")
    else:
        print(f"✨ Starting new timer for: {description}")
    
    # Always create a new timer (this is the most reliable approach)
    # Clockify will automatically handle the organization
    data = {
        "start": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "description": description,
        "projectId": PROJECT_ID
    }
    
    try:
        response = requests.post(
            f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/time-entries",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"▶️  Timer started: {description}")
            return True
        else:
            print(f"❌ Error starting timer: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting timer: {e}")
        return False

if __name__ == "__main__":
    # Test the smart timer
    test_description = "Se trabaja en Rama test"
    smart_start_timer(test_description)