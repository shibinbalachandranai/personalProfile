"""
Run this once to get your LinkedIn access token.
Usage: python get_token.py
"""

import http.server
import os
import threading
import urllib.parse
import webbrowser
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "openid profile w_member_social"

auth_code = None


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Authorization successful! You can close this tab.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>No code received. Try again.</h2>")

    def log_message(self, format, *args):
        pass  # Suppress request logs


def main():
    # Start local server to catch the redirect
    server = http.server.HTTPServer(("localhost", 8080), CallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    # Open LinkedIn authorization URL in browser
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}"
        f"&scope={urllib.parse.quote(SCOPE, safe='')}"
        f"&state=securestate123"
    )

    print("Opening LinkedIn authorization in your browser...")
    print(f"If it doesn't open, visit:\n{auth_url}\n")
    webbrowser.open(auth_url)

    thread.join(timeout=120)

    if not auth_code:
        print("Timed out waiting for authorization. Run the script again.")
        return

    # Exchange code for access token
    print("Exchanging code for access token...")
    response = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )

    if response.status_code != 200:
        print(f"Failed to get token: {response.status_code} {response.text}")
        return

    token_data = response.json()
    access_token = token_data.get("access_token")

    # Get person URN
    print("Fetching your LinkedIn Person URN...")
    me_response = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )

    person_urn = ""
    if me_response.status_code == 200:
        person_urn = me_response.json().get("id", "")
    else:
        print(f"Warning: could not fetch Person URN: {me_response.status_code} {me_response.text}")

    print("\n" + "=" * 60)
    print("SUCCESS — add these to your .env file:")
    print("=" * 60)
    print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
    if person_urn:
        print(f"LINKEDIN_PERSON_URN={person_urn}")
    else:
        print("LINKEDIN_PERSON_URN=<fetch manually via GET /v2/me>")
    print("=" * 60)


if __name__ == "__main__":
    main()
