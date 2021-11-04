from faker import Faker
from faker_airtravel import AirTravelProvider
import random
import requests

fake = Faker()
fake.add_provider(AirTravelProvider)

USER_URL = "http://localhost:8082/api/users"
FLIGHTS_URL = "http://localhost:8081/api/flights"
BOOKINGS_URL = "http://localhost:8083/api/bookings"
AUTH_URL = "http://localhost:8084/api/auth"


def add_user(token):
    for _ in range(100):
        user_data = {
            "userRole": random.choice([1, 2, 3, 4]),
            "givenName": fake.first_name(),
            "familyName": fake.last_name(),
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
            "phone": fake.phone_number(),
        }

        headers = {"Authorization": token}

        response = requests.post(f"{USER_URL}/add", json=user_data, headers=headers)
        if response.status_code != 201:
            print(response.status_code)
            print(response.json())
            break


def add_admin(token):
    user_data = {
        "userRole": 2,
        "givenName": fake.first_name(),
        "familyName": fake.last_name(),
        "username": "admin",
        "email": fake.email(),
        "password": "1234",  # fake.password(),
        "phone": fake.phone_number(),
    }

    headers = {"Authorization": token}

    response = requests.post(f"{USER_URL}/add", json=user_data, headers=headers)
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    up = {"username": "admin", "password": "1234"}
    res = requests.post(f"{AUTH_URL}/login", data=up)
    token = "Bearer " + res.json()["access_token"]
    print(token)
    add_user(token)
