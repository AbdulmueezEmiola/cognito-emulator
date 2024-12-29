from dotenv import load_dotenv
import os
import requests
import boto3
from lambda_functions.helpers import get_ssm_parameter

load_dotenv(override=True)


def handler(event, context):
    print(event)
    print(context)
    url = f"{os.getenv('URL')}/clinician/account/post-verification"
    given_name = event["request"]["userAttributes"]["given_name"]
    family_name = event["request"]["userAttributes"]["family_name"]
    email = event["request"]["userAttributes"]["email"]
    user_name = event["request"]["userAttributes"]["sub"]
    environment = os.getenv("ENVIRONMENT")

    payload = {
        "email": email,
        "last_name": family_name,
        "first_name": given_name,
        "auth_id": user_name,
    }

    headers = {"x-api-key": get_ssm_parameter(f"{environment.upper()}_API_KEY")}
    print(headers)
    response = requests.request("POST", url, json=payload, headers=headers)

    if not response.ok:
        print(response.status_code)
        print(response.json())
        raise Exception("Error in post verification api call")

    return event
