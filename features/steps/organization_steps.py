from behave import given, when, then
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app

client = TestClient(app)

@given('I have the organization feature set to "{feature_set}"')
def set_feature_set(context, feature_set):
    context.feature_set = feature_set

@when("I request to create a new organization")
def create_organization(context):
    response = client.post("/create_organization/", params={"feature_set": context.feature_set})
    assert response.status_code == 200
    context.response = response.json()

@then("I should receive a confirmation of the organization creation")
def organization_creation_confirmation(context):
    assert "Organization" in context.response

