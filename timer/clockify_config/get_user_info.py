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

# Get current user info
response = requests.get(
    "https://api.clockify.me/api/v1/user",
    headers=headers
)

if response.status_code == 200:
    user_info = response.json()
    print(f"User ID: {user_info['id']}")
    print(f"Name: {user_info['name']}")
    print(f"Email: {user_info['email']}")
    print(f"\nAdd this to your .env file:")
    print(f"CLOCKIFY_USER_ID={user_info['id']}")
else:
    print(f"Error: {response.status_code} - {response.text}")