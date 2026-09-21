import requests
r = requests.post(
    "http://127.0.0.1:8000/api/auth/signup/",
    json={"username": "alice", "email": "alice@example.com",
          "password": "9773878_qQ", "password2": "9773878_qQ"},
)
print(r.status_code, r.text)