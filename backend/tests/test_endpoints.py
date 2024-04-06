import requests

URL = "http://127.0.0.1:8080"


def test_add_user():
    response = requests.post(
        f"{URL}/users/",
        json={
            "nick": "test_nick",
            "is_premium": True,
            "experience": 10
        }
    )
    assert response.status_code == 200



def test_get_all_users():
    response = requests.get(f"{URL}/users/")
    assert response.status_code == 200
