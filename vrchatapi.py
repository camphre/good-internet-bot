import json
from pprint import pprint

import cloudscraper

import config
from two_factor_auth import get_two_factor_auth_code

BASE_URL = "https://api.vrchat.cloud/api/1"

data = {"apiKey": "JlE5Jldo5Jibnk5O5hTx6XVqsJu4WJ26"}  # Public API Key
headers = {"User-Agent": "SunaFH/1.0.5"}

scraper = cloudscraper.create_scraper()


def get_apiKey():
    response = scraper.get(f"{BASE_URL}/config")
    response.raise_for_status()
    apiKey = json.loads(response.text)["clientApiKey"]
    return apiKey


# Authentication


def login_and_get_current_user():
    response = scraper.get(
        BASE_URL + "/auth/user", data=data, auth=(config.username, config.password)
    )
    response.raise_for_status()
    return response.json()


def verify_2FA_code():
    data["code"] = get_two_factor_auth_code(config.totp)
    response = scraper.post(
        f"{BASE_URL}/auth/twofactorauth/totp/verify",
        data=data,
        auth=(config.username, config.password),
    )
    response.raise_for_status()
    return response.json()


def logout():
    reponse = scraper.put(f"{BASE_URL}/logout")
    reponse.raise_for_status()
    return reponse.json()


def auth(func):
    def wrapper(*args, **kwargs):
        verify_2FA_code()
        login_and_get_current_user()
        func(*args, **kwargs)
        logout()

    return wrapper


# Users


def get_user_by_username(username):
    response = scraper.get(f"{BASE_URL}/users/{username}/name", data=data)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if config.totp:
        verify_2FA_code()
    login_and_get_current_user()

    user = "ponpokoka"  # 調べたいusername
    res = get_user_by_username(user)
    print(f"{res['displayName']}({res['username']}) is {res['worldId']}")

    logout()
