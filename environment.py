from fastapi.testclient import TestClient
from app import app  # Import your FastAPI app

def before_all(context):
    context.client = TestClient(app)

