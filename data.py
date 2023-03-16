import requests
from deta import Base

from constants import basic_auth, REDIRECT_URI, API_BASE_URL

auth_base = Base("esporifai-auth")


def get_auth_code(code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    res = requests.post(
        url="https://accounts.spotify.com/api/token",
        data=data,
        headers=headers,
        auth=basic_auth,
    )

    if res.status_code == 200:
        auth_response = res.json()
        auth_base.put(
            key="access_token",
            data=auth_response["access_token"],
            expire_in=auth_response["expires_in"],
        )
        auth_base.put(key="refresh_token", data=auth_response["refresh_token"])
        auth_base.put(key="scope", data=auth_response["scope"])
        auth_base.put(key="token_type", data=auth_response["token_type"])
        return auth_response["access_token"]
    else:
        return None


def get_refreshed_token(token: str):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": token,
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }
    res = requests.post(
        url="https://accounts.spotify.com/api/token",
        data=data,
        headers=headers,
        auth=basic_auth,
    )

    if res.status_code == 200:
        print(res.json())
        auth_response = res.json()
        auth_base.put(
            key="access_token",
            data=auth_response["access_token"],
            expire_in=auth_response["expires_in"],
        )
        auth_base.put(key="scope", data=auth_response["scope"])
        auth_base.put(key="token_type", data=auth_response["token_type"])
        return auth_response["access_token"]
    else:
        return None


def retrieve_token():
    access_token = auth_base.get("access_token")
    refresh_token = auth_base.get("refresh_token")

    if not access_token:
        if refresh_token:
            access_token = get_refreshed_token(token=refresh_token["value"])
            return access_token
        else:
            return None

    return access_token["value"]


def get_user_profile():
    url = f"{API_BASE_URL}/me"
    access_token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    res = requests.get(url=url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return None