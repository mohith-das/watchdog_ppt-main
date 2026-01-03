# watchdog_ppt-main

Alerting/reporting pipeline that builds PPTs from anomaly outputs and shares them via Slack/Teams. Secrets are injected at runtime; none are stored in the repo.

## Components
- `anomaly_slide.py`, `create_ppt.py`: build slides/images.
- `send_ppt.py`: Slack/Teams/email delivery.
- `bigquery.py`: helper to fetch data locally.
- `cloudbuild.yaml`: example build/deploy config.

## Configure (env vars)
- `SLACK_BOT_TOKEN` – Slack bot token.
- `TEAMS_WEBHOOK_URL` – Teams webhook.
- `GOOGLE_APPLICATION_CREDENTIALS` or `SERVICE_ACCOUNT_FILE` – service account JSON if querying BigQuery.
- Any dataset/table IDs referenced in helper modules.

## Run locally
```bash
pip install -r requirements.txt  # if present
export SLACK_BOT_TOKEN=replace_me
export TEAMS_WEBHOOK_URL=replace_me
python anomaly_slide.py
```

## Notes
- Keep using mock/non-sensitive data for demos.
- Add retries/error handling before production deployments.
