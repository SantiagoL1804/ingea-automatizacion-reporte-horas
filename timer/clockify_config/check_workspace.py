#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('CLOCKIFY_API_KEY')
WORKSPACE_ID = os.getenv('CLOCKIFY_WORKSPACE_ID')

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

# Get workspace settings
try:
    response = requests.get(
        f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}",
        headers=headers
    )
    
    if response.status_code == 200:
        workspace = response.json()
        settings = workspace.get('workspaceSettings', {})
        
        print("🏢 Workspace Information:")
        print(f"Name: {workspace.get('name', 'N/A')}")
        print(f"ID: {workspace.get('id', 'N/A')}")
        
        print("\n⚙️  Workspace Settings:")
        print(f"Force Projects: {settings.get('forceProjects', 'Unknown')}")
        print(f"Force Tasks: {settings.get('forceTasks', 'Unknown')}")
        print(f"Force Tags: {settings.get('forceTags', 'Unknown')}")
        print(f"Force Description: {settings.get('forceDescription', 'Unknown')}")
        
        if settings.get('forceProjects'):
            print("\n💡 This workspace REQUIRES projects for time entries.")
        
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")