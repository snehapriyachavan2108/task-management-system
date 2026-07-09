import requests

from config import API_BASE_URL


class APIError(Exception):
    """Raised when a backend request fails."""


def _build_headers(token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def api_request(method, path, *, token=None, json_body=None, params=None):
    url = f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    try:
        response = requests.request(
            method,
            url,
            headers=_build_headers(token),
            json=json_body,
            params=params,
            timeout=10,
        )
    except requests.RequestException as exc:
        raise APIError(f"Unable to reach the API server: {exc}") from exc

    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise APIError(detail)

    if response.status_code == 204:
        return None

    try:
        return response.json()
    except ValueError:
        return response.text


def login_user(username, password):
    return api_request("POST", "/user/login", json_body={"username": username, "password": password})


def register_user(payload):
    return api_request("POST", "/user/register", json_body=payload)


def get_tasks(token):
    return api_request("GET", "/tasks/all_tasks", token=token)


def create_task(token, payload):
    return api_request("POST", "/tasks/create", token=token, json_body=payload)


def update_task(token, task_id, payload):
    return api_request("PUT", f"/tasks/update_task/{task_id}", token=token, json_body=payload)


def delete_task(token, task_id):
    return api_request("DELETE", f"/tasks/delete_task/{task_id}", token=token)
