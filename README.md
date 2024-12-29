# Setting Up Cognito for Local Development

## Requirements

- `sam cli`: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
- `docker`

## Setting Up Lambda Functions

To emulate the AWS Lambda environment locally, follow these steps from the project root:

1. Run `sam build` to build the SAM application.
2. Start the local Lambda environment with:
   ```bash
   sam local start-lambda --env-vars .env.json
   ```
   _(The `.env.json` file is a generic configuration file used to pass parameters to the `template.yaml` file.)_
3. Once the command runs successfully, you should see a message confirming that the API endpoint is available at:
   ```
   http://127.0.0.1:3001
   ```

## Setting Up Cognito Emulator for Local Development

1. **Install Dependencies**  
   Navigate to the `cognito-emulator` folder and install all required dependencies:

   ```bash
   npm i
   ```

2. **Start the Emulator**  
   Run the following command to start the Cognito emulator server:

   ```bash
   npx cognito-local
   ```

3. **User Pool Configuration**  
   By default, the user pool configured in the repository includes the following credentials:

   - **UserPoolId**: `local_2IhnSu1x`
   - **AppClientId**: `5k5ieatfoef9380ng8ug74znq`
   - **Endpoint URL**: `http://localhost:9229`

   Ensure these details are:

   - Configured in the **frontend environment** variables.
   - Updated in the **backend environment** variables.

## Miscellaneous

### Resetting the User Pool

To reset the user pool, follow these steps:

1.  **Delete the Database Folder**  
    Navigate to the `.cognito` folder inside the `cognito-emulator` directory and delete the `db` folder.

2.  **Create a New User Pool**  
     Run the following command to create a new user pool:

    ```bash
    aws --endpoint-url http://localhost:9229 cognito-idp create-user-pool \
        --pool-name LocalUserPool \
        --policies PasswordPolicy="{MinimumLength=8,RequireUppercase=true,RequireLowercase=true,RequireNumbers=true,RequireSymbols=true}" \
        --schema '[
            { "Name": "given_name", "AttributeDataType": "String", "Mutable": true, "Required": true },
            { "Name": "family_name", "AttributeDataType": "String", "Mutable": true, "Required": true },
            { "Name": "accountId", "AttributeDataType": "String", "Mutable": true, "Required": false }
        ]' \
        --auto-verified-attributes email \
        --alias-attributes email \
        --email-configuration EmailSendingAccount=DEVELOPER \
        --mfa-configuration OPTIONAL \
        --verification-message-template '{"DefaultEmailOption":"CONFIRM_WITH_LINK", "EmailSubject":"Your verification link", "EmailMessage":"Click on the link below to verify your email address: {##Verify Email##}"}'
    ```

    ```bash
        aws --endpoint-url http://localhost:9229 cognito-idp create-group  --group-name ADMIN --user-pool-id local_2IhnSu1x
        aws --endpoint-url http://localhost:9229 cognito-idp create-group  --group-name CLINICIAN --user-pool-id local_2IhnSu1x
        aws --endpoint-url http://localhost:9229 cognito-idp create-group  --group-name FACILITY --user-pool-id local_2IhnSu1x
    ```

    After executing this command, the **userPoolId** will be displayed in the terminal.

---

### Creating a User Pool Client

1. Use the **userPoolId** from the previous step and run the following command, replacing `<userPoolId>` with the actual ID:

   ```bash
   aws --endpoint-url http://localhost:9229 cognito-idp create-user-pool-client \
       --user-pool-id <userPoolId> \
       --client-name MyAppClient \
       --generate-secret \
       --explicit-auth-flows "ALLOW_USER_PASSWORD_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" \
       --callback-urls "http://localhost:3000/callback" \
       --logout-urls "http://localhost:3000/logout" \
       --supported-identity-providers "COGNITO"
   ```

2. The **clientId** will also be displayed in the terminal upon successful execution.

---

### Update Environment Variables

Ensure that both the `userPoolId` and `clientId` are updated in the frontend and backend environment variables.
