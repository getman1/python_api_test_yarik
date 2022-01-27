from ast import Pass
from urllib import request
import pytest
import requests
import json

root_url = "http://localhost:5000"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
create_user_payload = {
		"username": "User",
		"email": "test@test.com",
		"password": "123"
	}

def test_get_users():
	url = f"{root_url}/users"
	response = requests.get(url)
	body_type = type(response.json())
	expected_body_type = list

	assert body_type == expected_body_type

def test_create_user():
	url = f"{root_url}/users"
	response = requests.post(url, headers=headers, data=json.dumps(create_user_payload))
	assert response.status_code == 201
	user_id = response.json().get("id")

	user_url = f"{url}/{user_id}"
	response = requests.get(user_url)
	assert response.status_code == 200

	response_data = response.json()
	del response_data["id"]
	assert response_data == create_user_payload


def test_update_user():
    url = f"{root_url}/users"
    response = requests.post(url, headers=headers, data=json.dumps(create_user_payload))

    if response.status_code == 201:
        new_user_id = response.json().get("id")
        new_name = "resss"
        upd_user_payload = {"username": new_name}
        response = requests.put(f"{url}/{new_user_id}", headers=headers, data=json.dumps(upd_user_payload))
        print(response.text)
        assert response.status_code == 201

        user_url = f"{url}/{new_user_id}"

        get_user_response = requests.get(user_url)
        assert get_user_response.json().get("username") == new_name
