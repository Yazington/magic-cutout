import requests
import hmac
import hashlib
import os
import sys
from pyrfc3339 import generate
from datetime import datetime, timezone

from body import ApplicationSubmission

print("Starting B12 submission...", file=sys.stdout, flush=True)

url = "https://b12.io/apply/submission"

# Get action_run_link from GitHub Actions environment variables
github_server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
github_repository = os.getenv("GITHUB_REPOSITORY", "Yazington/magic-cutout")
github_run_id = os.getenv("GITHUB_RUN_ID", "local-run")

action_run_link = f"{github_server_url}/{github_repository}/actions/runs/{github_run_id}"

print(f"Action Run Link: {action_run_link}", file=sys.stdout, flush=True)

submission = ApplicationSubmission(
    timestamp=generate(datetime.now(timezone.utc)),
    name="Yazan Maarouf",
    email="yazan.maarouf.1@gmail.com",
    resume_link="https://www.linkedin.com/in/yazanmaarouf/",
    repository_link="https://github.com/Yazington/magic-cutout",
    action_run_link=action_run_link,
)

body = submission.to_json()

print(f"Request Body: {body}", file=sys.stdout, flush=True)

signing_secret = (
    "hello-there-from-b12"  # normally, comes from env var or secret manager
)
signature = hmac.new(
    signing_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
).hexdigest()

print(f"Signature: {signature}", file=sys.stdout, flush=True)

try:
    response = requests.post(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "charset": "utf-8",
            "X-Signature-256": f"sha256={signature}",
        },
    )

    print(f"Status Code: {response.status_code}", file=sys.stdout, flush=True)
    print(f"Response: {response.text}", file=sys.stdout, flush=True)
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr, flush=True)
    sys.exit(1)
