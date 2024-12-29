import boto3
import os


def get_ssm_parameter(param_name):
    """Fetch a parameter value from AWS SSM Parameter Store."""
    try:
        ssm = boto3.client("ssm", region_name=os.getenv("REGION"))
        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except Exception as e:
        print(f"Error fetching SSM parameter {param_name}: {e}")
        raise e
