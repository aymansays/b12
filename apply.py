import requests
import datetime
import hmac
import hashlib
import json
import os

# Fetch signing secret key
try:
    SIGNING_SECRET = os.environ["SIGNING_SECRET"]
except KeyError:
    SIGNING_SECRET = "hello-there-from-b12"

def generatePayload():
    # timestamp = datetime.datetime.now().isoformat()
    timestamp = "2026-01-06T16:59:37.571Z"
    name = "Your name"
    email = "you@example.com"
    resumeLink = "https://pdf-or-html-or-linkedin.example.com"
    repoLink = "https://link-to-github-or-other-forge.example.com/your/repository"
    actionRunLink = "https://link-to-github-or-another-forge.example.com/your/repository/actions/runs/run_id"

    payload = dict(sorted({
        "timestamp": timestamp,
        "name": name,
        "email": email,
        "resume_link": resumeLink,
        "repository_link": repoLink,
        "action_run_link": actionRunLink
    }.items()))

    payload = json.dumps(payload).replace(", ", ",").replace(": ", ":")

    return payload

def generateHeaders(key, payload):
    sha256 = hmac.new(key.encode(), payload.encode(), hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={sha256}"
    }

    return headers

def main():
    url = "https://b12.io/apply/submission"

    payload = generatePayload()
    print(payload)

    headers = generateHeaders(SIGNING_SECRET, payload)
    print(headers)

    response = requests.post(
        url,
        data=payload,
        headers=headers,
        timeout=10
    )

    # Check response
    print("Status code:", response.status_code)
    print("Response body:", response.text)

    if response.headers.get("Content-Type", "").startswith("application/json"):
        print(response.json())


if __name__ == "__main__":
    main()
