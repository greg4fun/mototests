from fastapi import FastAPI, HTTPException
from moto import mock_organizations
import boto3
from botocore.exceptions import ClientError

app = FastAPI()

# Start the mock for organizations
mock_orgs = mock_organizations()
mock_orgs.start()

# Create a client to interact with what moto has mocked.
client = boto3.client("organizations", region_name="us-east-1")

@app.post("/create_organization/")
async def create_organization():
    try:
        response = client.create_organization(FeatureSet='ALL')
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create_account/")
async def create_account(email: str, account_name: str):
    try:
        response = client.create_account(
            Email=email,
            AccountName=account_name
        )
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/close_account/")
async def close_account(account_id: str):
    try:
        # Moto doesn't support closing an account directly. 
        # Here we mimic the behavior by removing an account from the organization.
        # In a real scenario, this would require AWS to support the operation.
        response = client.close_account(AccountId=account_id)
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
@app.get("/list_organizations/")
async def list_organizations():
    try:
        # Use the moto mock to list organizations
        response = client.list_organizations()
        return response
    except ClientError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Use this to stop the mock after you are done
@app.on_event("shutdown")
def shutdown_event():
    mock_orgs.stop()

