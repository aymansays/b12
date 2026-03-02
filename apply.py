import requests
import datetime
import hmac
import hashlib
import json
import os

# Fetch signing secret key & github actions run id
try:
    SIGNING_SECRET = os.environ["SIGNING_SECRET"]
    RUN_ID = os.environ["RUN_ID"]
except KeyError:
    SIGNING_SECRET = "hello-there-from-b12"
    RUN_ID = 0

def generatePayload():
    timestamp = datetime.datetime.now().isoformat()
    name = "Ayman Faisal"
    email = "aymanfaisal7@gmail.com"
    resumeLink = "https://www.linkedin.com/in/ayman-faisal"
    repoLink = "https://github.com/aymansays/b12"
    actionRunLink = f"https://github.com/aymansays/b12/actions/runs/{RUN_ID}"

    payload = dict(sorted({
        "timestamp": timestamp,
        "name": name,
        "email": email,
        "resume_link": resumeLink,
        "repository_link": repoLink,
        "action_run_link": actionRunLink
    }.items()))

    # Canonicalize payload
    payload = json.dumps(payload).replace(", ", ",").replace(": ", ":")

    return payload

def generateHeaders(key, payload):
    # Create hex digest of payload using signing secret
    sha256 = hmac.new(key.encode(), payload.encode(), hashlib.sha256).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={sha256}"
    }

    return headers

def main():
    # Create POST request
    url = "https://b12.io/apply/submission"

    payload = generatePayload()
    print(payload)

    headers = generateHeaders(SIGNING_SECRET, payload)
    print(headers)

    # Send POST request
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
