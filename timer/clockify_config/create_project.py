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

# Create a default project
project_data = {
    "name": "INGEA Development",
    "color": "#0099CC",
    "isPublic": False
}

try:
    response = requests.post(
        f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects",
        headers=headers,
        json=project_data
    )
    
    if response.status_code == 201:
        project = response.json()
        print("✅ Project created successfully!")
        print(f"Project ID: {project['id']}")
        print(f"Project Name: {project['name']}")
        print(f"\n💡 Add this to your .env file:")
        print(f"CLOCKIFY_PROJECT_ID={project['id']}")
    else:
        print(f"❌ Error creating project: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")