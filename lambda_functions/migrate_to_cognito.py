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
    ssm = boto3.client("ssm", region_name=os.getenv("REGION"))
    base_url = os.getenv("URL")
    environment = os.getenv("ENVIRONMENT")
    if not base_url:
        raise Exception("Base URL is not defined. Check environment variables.")
    url = f"{base_url}/base/migration/migrate-to-cognito"
    headers = {"x-api-key": get_ssm_parameter(ssm, f"{environment.upper()}_API_KEY")}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return event
    else:
        print(f"Failed to complete migration: {response.status_code}")
        raise Exception("Failed to complete migration. Please try again later.")
