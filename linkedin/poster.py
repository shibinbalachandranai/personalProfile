import requests
import config


class LinkedInPostError(Exception):
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"LinkedIn API error {status_code}: {body}")


def post_to_linkedin(text: str) -> dict:
    """
    Publish text as a LinkedIn UGC post.

    Returns the parsed JSON response from the LinkedIn API on success.
    Raises LinkedInPostError on failure.
    """
    token = config.LINKEDIN_ACCESS_TOKEN
    urn = config.LINKEDIN_PERSON_URN

    if not token:
        raise LinkedInPostError(0, "LINKEDIN_ACCESS_TOKEN is not set in .env")
    if not urn:
        raise LinkedInPostError(0, "LINKEDIN_PERSON_URN is not set in .env")

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }
    payload = {
        "author": f"urn:li:person:{urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text,
                },
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
    except requests.RequestException as e:
        raise LinkedInPostError(0, f"Network error: {e}") from e

    if response.status_code == 401:
        raise LinkedInPostError(
            401,
            "Unauthorized — your LinkedIn access token may have expired. "
            "Refresh it at developer.linkedin.com and update .env.",
        )

    if response.status_code != 201:
        raise LinkedInPostError(response.status_code, response.text)

    return response.json()
