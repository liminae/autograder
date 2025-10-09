import requests
from bs4 import BeautifulSoup

LOGIN_URL = "http://127.0.0.1:3000/djangoadmin/login/"
TARGET_URL = "http://127.0.0.1:3000/status/process_submit/"
REQUESTS_TO_SEND = 25

USERNAME = "admin"
PASSWORD = "123"

with open("example_sol.java", "r") as f:
    code_contents = f.read()

post_data = {"problemid": "1", "lang": "java", "code": code_contents}


def authenticate_and_send_requests(username, password, target_url, data, num_requests):
    with requests.Session() as s:
        print("Attempting to log in...")

        print("Fetching login page and CSRF token...")
        try:
            get_response = s.get(LOGIN_URL)
            get_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch login page: {e}")
            return

        soup = BeautifulSoup(get_response.text, "html.parser")
        login_csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        login_payload = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": login_csrf_token,
            "next": "",
        }

        try:
            login_response = s.post(LOGIN_URL, data=login_payload)
            login_response.raise_for_status()
            if "Please enter the correct username and password" in login_response.text:
                print("Login failed: Invalid username or password.")
                return
            print(f"Login successful! Status code: {login_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return

        try:
            csrf_token_for_posts = s.cookies["csrftoken"]
            data["csrfmiddlewaretoken"] = csrf_token_for_posts
        except KeyError:
            print("Failed to find 'csrftoken' in session cookies after login.")
            return

        print(
            f"\nStarting to send {num_requests} authenticated requests to {target_url}"
        )
        for i in range(num_requests):
            try:
                response = s.post(target_url, data=data)
                response.raise_for_status()
                print(f"Request successful! Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                break

    print("\nFinished sending all requests.")


if __name__ == "__main__":
    authenticate_and_send_requests(
        USERNAME, PASSWORD, TARGET_URL, post_data, REQUESTS_TO_SEND
    )
