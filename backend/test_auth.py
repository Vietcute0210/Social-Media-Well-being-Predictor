import requests

# Test register
print("Testing /auth/register...")
response = requests.post(
    "http://localhost:8000/auth/register",
    json={"username": "testuser123", "password": "123456"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
