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


# 1
def test_add_journey():
    response = requests.post(
        f"{URL}/journeys/",
        json={
            "user_id": 1,
            "duration": 10
        }
    )
    assert response.status_code == 200

def test_add_journey_with_start_time():
    response = requests.post(
        f"{URL}/journeys/",
        json={
            "user_id": 1,
            "duration": 10,
            "start_date": "2021-10-10T10:10:10"
        }
    )
    assert response.status_code == 200
def test_get_all_journeys():
    response = requests.get(f"{URL}/journeys/1")
    res = response.json()
    assert response.status_code == 200


def test_delete_journey():
    response = requests.post(
        f"{URL}/journeys/2"
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Journey deleted successfully"}