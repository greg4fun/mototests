from fastapi import FastAPI, HTTPException, Query
from moto import mock_organizations
import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel

app = FastAPI()

# Start the mock for organizations
mock_orgs = mock_organizations()
mock_orgs.start()

# Create a client to interact with what moto has mocked.
client = boto3.client("organizations", region_name="us-east-1")

@app.post("/create_organization/")
async def create_organization(feature_set: str = "ALL"):
    try:
        response = client.create_organization(FeatureSet=feature_set)
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create_account/")
async def create_account(email: str, account_name: str):
    try:
        print(300*'-')
        print(email,account_name)
        #client.create_organization(FeatureSet='ALL')
        response = client.create_account(
            Email=email,
            AccountName=account_name
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/list_accounts/")
async def list_accounts():
    try:
        response = client.list_accounts()
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/invite_account_to_organization/")
async def invite_account_to_organization(target_email: str):
    try:
        response = client.invite_account_to_organization(
            Target={
                'Type': 'EMAIL',
                'Id': target_email
            }
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/accept_handshake/")
async def accept_handshake(handshake_id: str):
    try:
        response = client.accept_handshake(
            HandshakeId=handshake_id
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/decline_handshake/")
async def decline_handshake(handshake_id: str):
    try:
        response = client.decline_handshake(
            HandshakeId=handshake_id
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/remove_account_from_organization/")
async def remove_account_from_organization(account_id: str):
    try:
        response = client.remove_account_from_organization(
            AccountId=account_id
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/describe_organization/")
async def describe_organization():
    try:
        response = client.describe_organization()
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/describe_account/")
async def describe_account(account_id: str):
    try:
        response = client.describe_account(
            AccountId=account_id
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/list_accounts_for_parent/")
async def list_accounts_for_parent(parent_id: str):
    try:
        response = client.list_accounts_for_parent(
            ParentId=parent_id
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/list_roots/")
async def list_roots():
    try:
        response = client.list_roots()
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

class CloseAccountRequest(BaseModel):
    account_id: str

@app.post("/close_account/")
def close_account(request: CloseAccountRequest):
    with mock_organizations():
        client = boto3.client("organizations")
        try:
            # Since this is a mock, it won't actually perform any operation.
            # Moto does not fully implement organizations, and this is just a placeholder.
            # In a real AWS environment, you would call client.close_account
            # with the necessary parameters and handle the response.
            # The following line is just for illustration and will not close any account.
            response = client.close_account(AccountId=request.account_id)

            return {"Status": "Account closed successfully.", "Response": response}

        except client.exceptions.AWSOrganizationsNotInUseException:
            raise HTTPException(status_code=403, detail="AWS Organizations is not in use.")
        except client.exceptions.AccountNotFoundException:
            raise HTTPException(status_code=404, detail="Account not found.")
        except Exception as e:
            # Catch any other exceptions that might occur and return as HTTP errors
            raise HTTPException(status_code=500, detail=str(e))
@app.on_event("shutdown")
def shutdown_event():
    mock_orgs.stop()
