import requests
import hmac
import hashlib
import os
from pyrfc3339 import generate
from datetime import datetime, timezone

from body import ApplicationSubmission

url = "https://b12.io/apply/submission"

# Get action_run_link from GitHub Actions environment variables
github_server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")
github_repository = os.getenv("GITHUB_REPOSITORY", "Yazington/magic-cutout")
github_run_id = os.getenv("GITHUB_RUN_ID", "local-run")

action_run_link = f"{github_server_url}/{github_repository}/actions/runs/{github_run_id}"

submission = ApplicationSubmission(
    timestamp=generate(datetime.now(timezone.utc)),
    name="Yazan Maarouf",
    email="yazan.maarouf.1@gmail.com",
    resume_link="https://www.linkedin.com/in/yazanmaarouf/",
    repository_link="https://github.com/Yazington/magic-cutout",
    action_run_link=action_run_link,
)

body = submission.to_json()

signing_secret = (
    "hello-there-from-b12"  # normally, comes from env var or secret manager
)
signature = hmac.new(
    signing_secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
).hexdigest()

requests.post(
    url,
    data=body,
    headers={
        "Content-Type": "application/json",
        "charset": "utf-8",
        "X-Signature-256": f"sha256={signature}",
    },
)
