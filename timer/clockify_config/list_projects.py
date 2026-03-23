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

# Get projects
try:
    response = requests.get(
        f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects",
        headers=headers
    )
    
    if response.status_code == 200:
        projects = response.json()
        print("📋 Available projects:")
        print("-" * 50)
        for project in projects:
            print(f"ID: {project['id']}")
            print(f"Name: {project['name']}")
            print(f"Color: {project.get('color', 'N/A')}")
            print(f"Archived: {project.get('archived', False)}")
            print(f"Public: {project.get('public', False)}")
            print("-" * 30)
        
        if projects:
            print(f"\n💡 Add this to your .env file:")
            print(f"CLOCKIFY_PROJECT_ID={projects[0]['id']}")
            print(f"\n(Using first project: '{projects[0]['name']}')")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")