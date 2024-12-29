from dotenv import load_dotenv
import os

load_dotenv(override=True)


def handler(event, context):
    print("Event:", event)
    print("Context:", context)
    trigger_source = event["triggerSource"]
    username = event["request"]["userAttributes"]["sub"]
    code_parameter = event["request"]["codeParameter"]
    first_name = event["request"]["userAttributes"]["given_name"]
    url = os.getenv("URL")

    if trigger_source == "CustomMessage_ForgotPassword":
        event["response"]["emailSubject"] = "Password Recovery"
        event["response"]["emailMessage"] = get_forgot_password_message(
            username, code_parameter, first_name, url
        )
    elif trigger_source == "CustomMessage_SignUp":
        event["response"]["emailSubject"] = "Verify Your Email"
        event["response"]["emailMessage"] = get_sign_up_message(
            username, code_parameter, first_name, url
        )
    elif trigger_source == "CustomMessage_AdminCreateUser":
        event["response"]["emailSubject"] = "Welcome, Activate Your Account Today!"
        event["response"]["emailMessage"] = get_create_user_message(first_name, url)

    elif trigger_source == "CustomMessage_ResendCode":
        event["response"]["emailSubject"] = "Resend Verification Code"
        event["response"]["emailMessage"] = get_sign_up_message(
            username, code_parameter, first_name, url
        )

    return event


def get_forgot_password_message(username, code_parameter, email, url):
    return f"""<p>Hello {email}</p>
                <br/>
                <p>We've received a request to reset your password for your account. To proceed with the password reset, please click on the button below.</p>
                <br/>
                <a href='{url}/reset-password?code={code_parameter}&username={username}'>Reset Password</a>
                <br/>
                <p>If you didn't request this password reset, you can ignore this email.</p>
                <br/>
                <p>Thank you,</p>"""


def get_sign_up_message(username, code_parameter, email, url):
    return f"""<p>Hey {email}</p>
                <br/>
                <p>Thank you for joining us. Before we get started, you‘ll have to confirm your email address.</p>
                <br/>
                <p>Click on the button below to verify your email address and you‘re officially one of us!</p>
                <br/>
                <a href='{url}/verify?code={code_parameter}&username={username}'>Confirm your account</a>"""


def get_create_user_message(name, url):
    return f"""<p>Hey {name}</p>
                <br/>
                <p>Welcome!, We’re excited to have you as part of our community.</p>
                <br/>
                <p>Click on the button below to verify your email address and you‘re officially one of us!</p>
                <br/>
                <a href="{url}/invite?code={{####}}&username={{username}}" 
                        style="display: inline-block; background-color: #00124e; color: white; text-decoration: none; padding: 20px 40px; line-height: 120%; font-weight: bold;">Activate Account Now</a>"""
