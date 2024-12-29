from dotenv import load_dotenv
import os
import requests
import boto3
from lambda_functions.helpers import get_ssm_parameter

# Load environment variables from .env file
load_dotenv(override=True)


def handler(event, context):
    print("Event:", event)
    print("Context:", context)

    user_name = event["request"]["userAttributes"]["sub"]
    base_url = os.getenv("URL")
    environment = os.getenv("ENVIRONMENT")

    if not base_url:
        raise Exception("Base URL is not defined. Check environment variables.")

    url = f"{base_url}/base/authentication/post-authentication"

    payload = {"authId": user_name}
    headers = {"x-api-key": get_ssm_parameter(f"{environment.upper()}_API_KEY")}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return event
    else:
        print(f"Failed to verify user: {response.status_code}")
        raise Exception("Failed to verify user. Please try again later.")
