#!/usr/bin/env python3
import requests
import os
import subprocess
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_current_git_branch(repo_path=os.getenv("REPO_PATH", ".")):
    """Get the current git branch from the specified repository"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            branch_name = result.stdout.strip().replace('-', ' ').replace('_', ' ')
            return branch_name if branch_name else "main"
        else:
            return None
    except Exception as e:
        print(f"⚠️  Error getting git branch: {e}")
        return None

def get_current_running_timer():
    """Get the currently running timer from Clockify"""
    API_KEY = os.getenv('CLOCKIFY_API_KEY')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
    USER_ID = os.getenv('CLOCKIFY_USER_ID')
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries?in-progress=true",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            time_entries = response.json()
            if time_entries:
                return time_entries[0]  # First entry is the running one
        return None
        
    except Exception as e:
        print(f"❌ Error getting current timer: {e}")
        return None

def stop_current_timer():
    """Stop the current running timer"""
    API_KEY = os.getenv('CLOCKIFY_API_KEY')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
    USER_ID = os.getenv('CLOCKIFY_USER_ID')
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "end": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }
    
    try:
        response = requests.patch(
            f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            duration = result.get('timeInterval', {}).get('duration', 'N/A')
            description = result.get('description', 'N/A')
            print(f"⏹️  Timer stopped: {description} (Duration: {duration})")
            return True
        else:
            print(f"❌ Error stopping timer: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error stopping timer: {e}")
        return False

def find_latest_timer_with_description(description):
    """Find the most recent timer with matching description"""
    API_KEY = os.getenv('CLOCKIFY_API_KEY')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
    USER_ID = os.getenv('CLOCKIFY_USER_ID')
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/user/{USER_ID}/time-entries?page-size=20",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            timers = response.json()
            for timer in timers:
                if timer['description'] == description:
                    return timer
        return None
        
    except Exception as e:
        print(f"⚠️  Error finding existing timer: {e}")
        return None

def start_timer(description):
    """Start a new Clockify timer with given description (with smart detection)"""
    API_KEY = os.getenv('CLOCKIFY_API_KEY')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
    PROJECT_ID = os.getenv('CLOCKIFY_PROJECT_ID')
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Check if there's a recent timer with the same description
    existing_timer = find_latest_timer_with_description(description)
    
    if existing_timer:
        last_end = existing_timer['timeInterval']['end']
        if last_end:
            last_end_time = datetime.fromisoformat(last_end.replace('Z', '+00:00'))
            time_diff = datetime.now(timezone.utc) - last_end_time
            hours_since = time_diff.total_seconds() / 3600
            
            if hours_since < 2:  # Less than 2 hours ago
                print(f"🔄 Continuing recent work session (ended {int(hours_since*60)}min ago)")
            elif hours_since < 24:  # Less than 24 hours ago
                print(f"🔄 Resuming work from earlier today ({hours_since:.1f}h ago)")
            else:
                print(f"🔄 Resuming work on same task from {hours_since:.0f}h ago")
        else:
            print(f"⚠️  Found running timer with same description")
    else:
        print(f"✨ Starting fresh timer for new task")
    
    # Create new timer
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

def get_stored_branch():
    """Get the last stored branch name"""
    branch_file = "/home/santiago/ingea-automatizacion-reporte-horas/timer/logs/.last_branch"
    try:
        with open(branch_file, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def store_branch(branch_name):
    """Store the current branch name"""
    branch_file = "/home/santiago/ingea-automatizacion-reporte-horas/timer/logs/.last_branch"
    with open(branch_file, 'w') as f:
        f.write(branch_name)

def monitor_branch_changes():
    """Monitor for branch changes and manage timers accordingly"""
    print("🔍 Starting branch monitor...")
    
    current_branch = get_current_git_branch()
    if not current_branch:
        print("❌ Could not detect git branch. Exiting.")
        return
    
    stored_branch = get_stored_branch()
    
    # If no stored branch, this is the first run
    if not stored_branch:
        if current_branch != "main":
            description = f"Se trabaja en {current_branch}"
            if start_timer(description):
                store_branch(current_branch)
                print(f"🌿 Initial timer started for branch: {current_branch}")
        else:
            print("🌿 On main branch - no timer started")
        return
    
    # Check if branch has changed
    if current_branch != stored_branch:
        print(f"🔄 Branch changed: {stored_branch} → {current_branch}")
        
        # Stop current timer if there's one running
        current_timer = get_current_running_timer()
        if current_timer:
            print(f"⏹️  Stopping timer for: {current_timer.get('description', 'Unknown')}")
            stop_current_timer()
        
        # Start new timer if not on main
        if current_branch != "main":
            description = f"Se trabaja en {current_branch}"
            if start_timer(description):
                store_branch(current_branch)
                print(f"✅ Successfully switched timer to: {current_branch}")
        else:
            store_branch(current_branch)
            print("🌿 Switched to main branch - no timer started")
    else:
        print(f"✅ No branch change detected (still on: {current_branch})")

if __name__ == "__main__":
    monitor_branch_changes()