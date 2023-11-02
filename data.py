from datetime import datetime as dt

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


def delete_auth_data():
    auth_base.delete("access_token")
    auth_base.delete("refresh_token")


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


def get_user_playlists(limit: int = 20):
    url = f"{API_BASE_URL}/me/playlists?limit={limit}"
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


def get_user_top_artists(time_range: str = "short_term"):
    url = f"{API_BASE_URL}/me/top/artists?time_range={time_range}"
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


def get_user_top_tracks(time_range: str = "short_term"):
    url = f"{API_BASE_URL}/me/top/tracks?time_range={time_range}"
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


def get_playlist_by_id(playlist_id: str):
    url = f"{API_BASE_URL}/playlists/{playlist_id}"
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


def get_audio_features_from_ids(ids: str):
    url = f"{API_BASE_URL}/audio-features?{ids}"
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


def get_audio_features_by_id(trackid: str):
    url = f"{API_BASE_URL}/audio-features/{trackid}"
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


def get_user_recently_played(limit: int = 50):
    url = f"{API_BASE_URL}/me/player/recently-played"
    access_token = retrieve_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    params = {"limit": limit, "before": int(dt.now().timestamp() * 1000)}

    res = requests.get(url=url, headers=headers, params=params)
    if res.status_code == 200:
        return res.json()
    else:
        return None


def get_track_by_id(trackid: str):
    url = f"{API_BASE_URL}/tracks/{trackid}"
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
