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

    environment = os.getenv("ENVIRONMENT")
    headers = {"x-api-key": get_ssm_parameter(f"{environment.upper()}_API_KEY")}
    user_name = event["request"]["userAttributes"]["sub"]
    trigger_source = event["triggerSource"]
    if trigger_source == "TokenGeneration_RefreshTokens":
        return event
    user_groups = event["request"]["groupConfiguration"].get("groupsToOverride", [])
    payload = {"auth_id": user_name}
    if not user_groups:
        url = f"{os.getenv('URL')}/base/authentication/sync-user-groups"
        response = requests.request("POST", url, json=payload, headers=headers)
        if not response.ok:
            print(response.status_code)
            raise Exception("Error in post verification api call")
        synced_groups = response.json()
        user_groups.append(synced_groups)
        event["request"]["groupConfiguration"]["groupsToOverride"] = user_groups

    route = get_route(user_groups)
    url = construct_url(route)

    if send_auth_request(url, headers, payload):
        print(event)
        return event


def get_route(user_groups):
    """
    Factory function to determine the route based on user groups.
    """
    routes = {
        "STUDENT": "STUDENT",
        "TEACHER": "ADMIN",
    }

    for group in user_groups:
        if group in routes:
            return routes[group]

    print("User group not recognized.")
    raise Exception("Unauthorized: User group not recognized.")


def construct_url(route):
    """
    Construct the full URL using the base URL and route.
    """
    base_url = os.getenv("URL")
    if not base_url:
        raise Exception("Base URL is not defined. Check environment variables.")
    return f"{base_url}/{route}/account/pre-authentication"


def send_auth_request(url, headers, payload):
    """
    Send a POST request for authentication and handle response.
    """
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return True
        else:
            print(f"Failed to verify user: {response.status_code}")
            raise Exception("Failed to verify user. Please try again later.")

    except requests.RequestException as e:
        print(f"Request error: {e}")
        raise Exception("Could not complete pre-authentication check due to an error.")
