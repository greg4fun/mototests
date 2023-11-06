from fastapi.testclient import TestClient
from moto import mock_organizations
import pytest
from main import app  # Import the FastAPI instance from your app module

client = TestClient(app)

@mock_organizations
def test_create_organization():
    response = client.post("/create_organization/")
    assert response.status_code == 200
    assert "Organization" in response.json()

@mock_organizations
def test_create_account():
    response = client.post("/create_account/", json={"email": "test@example.com", "account_name": "Test Account"})
    assert response.status_code == 200
    assert "CreateAccountStatus" in response.json()

@mock_organizations
def test_list_accounts():
    # Create an account first to list
    client.post("/create_account/", json={"email": "test@example.com", "account_name": "Test Account"})
    response = client.get("/list_accounts/")
    assert response.status_code == 200
    assert "Accounts" in response.json()

@mock_organizations
def test_invite_account_to_organization():
    # Invite an account (mocked) to the organization
    response = client.post("/invite_account_to_organization/", json={"target_email": "invitee@example.com"})
    assert response.status_code == 200
    assert "Handshake" in response.json()

@mock_organizations
def test_accept_handshake():
    # To accept a handshake, one must exist. This would be more complex to mock correctly.
    # Here's a placeholder for how the test might look:
    response = client.post("/accept_handshake/", json={"handshake_id": "h-example"})
    assert response.status_code == 200
    # Assertions here would depend on how `moto` mocks handshake acceptances.

# ... Continue writing tests for other endpoints in a similar fashion.

# It's important to use the mock_organizations decorator to ensure the AWS services are mocked correctly.

