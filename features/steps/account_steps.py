from behave import given, when, then, step
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
import json

client = TestClient(app)

# Use this context to store data between steps
context = {}

@given('I have organization details')
def step_impl(context):
    # Presuming an organization creation feature has been implemented
    # and we have mocked it correctly using moto
    context.organization = {
        "FeatureSet": "ALL"
    }

@when('I create a new account with email "{email}" and account name "{account_name}"')
def step_impl(context, email, account_name):
    #client.post("/create_organization/", params={"feature_set": 'All'})
    response = client.post("/create_account/", json={"email": email, "account_name": account_name})
    assert response.status_code == 200
    context.create_account_response = response.json()

@then('the account should be successfully created')
def step_impl(context):
    assert "CreateAccountStatus" in context.create_account_response

@given('I have an existing account with email "{email}"')
def step_impl(context, email):
    # You need to handle the actual account creation and retrieval here
    # For now, let's assume the email is enough to identify the account
    context.account_email = email

@when('I invite the account with email "{email}" to the organization')
def step_impl(context, email):
    response = client.post("/invite_account_to_organization/", json={"target_email": email})
    assert response.status_code == 200
    context.invite_response = response.json()

@then('the invitation should be successfully sent')
def step_impl(context):
    assert "Handshake" in context.invite_response

@given('I have an existing account with id "{account_id}"')
def step_impl(context, account_id):
    context.account_id = account_id

@when('I close the account with id "{account_id}"')
def step_impl(context, account_id):
    response = client.post("/close_account/", json={"account_id": account_id})
    assert response.status_code == 200
    context.close_account_response = response.json()

@then('the account should be successfully closed')
def step_impl(context):
    assert context.close_account_response['Success']  # Adjust based on actual response structure

@when('I request to list accounts in the organization')
def step_impl(context):
    response = client.get("/list_accounts/")
    assert response.status_code == 200
    context.list_accounts_response = response.json()

@then('I should receive a list of accounts')
def step_impl(context):
    assert "Accounts" in context.list_accounts_response
