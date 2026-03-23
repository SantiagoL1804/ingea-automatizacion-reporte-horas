#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timezone
import sys
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_current_git_branch(repo_path="/home/santiago/Desktop/INGEA/sinuy-ing"):
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
            print(f"⚠️  Warning: Could not get git branch: {result.stderr.strip()}")
            return "no-branch"
    except subprocess.TimeoutExpired:
        print("⚠️  Warning: Git command timed out")
        return "timeout"
    except FileNotFoundError:
        print("⚠️  Warning: Git not found")
        return "no-git"
    except Exception as e:
        print(f"⚠️  Warning: Error getting git branch: {e}")
        return "error"

def start_clockify_timer(description=None):
    """Start a Clockify timer with given description or auto-detect from git branch"""
    
    # Auto-detect description from git branch if not provided
    if description is None:
        branch_name = get_current_git_branch()
        description = f"Se trabaja en {branch_name}"
        print(f"🌿 Detected git branch: {branch_name}")
    
    API_KEY = os.getenv('CLOCKIFY_API_KEY')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')
    PROJECT_ID = os.getenv('CLOCKIFY_PROJECT_ID')
    if not API_KEY or not WORKSPACE_ID:
        print("❌ Error: Please set CLOCKIFY_API_KEY and CLOCKIFY_WORKSPACE_ID environment variables")
        print("Or edit this script to include your API key and workspace ID directly")
        return False
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Data for starting the timer
    data = {
        "start": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "description": description,
        "projectId": PROJECT_ID,
        # Optional: add task_id, tag_ids here
        # "taskId": "TASK_ID",
        # "tagIds": ["TAG_ID1", "TAG_ID2"]
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
            print(f"✅ Timer started successfully!")
            print(f"   Description: {description}")
            print(f"   Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Timer ID: {result.get('id', 'N/A')}")
            return True
        else:
            print(f"❌ Error starting timer: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def stop_current_timer():
    """Stop the current running timer"""
    API_KEY = os.getenv('CLOCKIFY_API_KEY', 'YOUR_API_KEY_HERE')
    WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID', 'YOUR_WORKSPACE_ID_HERE')
    USER_ID = os.getenv('CLOCKIFY_USER_ID', 'YOUR_USER_ID_HERE')
    
    if any(val.startswith('YOUR_') for val in [API_KEY, WORKSPACE_ID, USER_ID]):
        print("❌ Error: Missing environment variables for stopping timer")
        return False
    
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
            json=data
        )
        
        if response.status_code == 200:
            print(f"✅ Timer stopped successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            return True
        else:
            print(f"❌ Error stopping timer: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error stopping timer: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        
        if action == "start":
            description = sys.argv[2] if len(sys.argv) > 2 else None
            start_clockify_timer(description)
        elif action == "stop":
            stop_current_timer()
        else:
            print("Usage: python clockify_timer.py [start|stop] [description]")
    else:
        # Default: start timer with auto-detected git branch
        start_clockify_timer()
