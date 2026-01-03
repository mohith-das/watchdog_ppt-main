from create_ppt import create_ppt
from config import in_production
import base64
import json
from send_ppt import send_ppt_to_slack
from dates import yesterday, get_previous_week_start_date_end_date
from hourly import send_hourly_alerts
from data_recency import send_data_recency_alerts
import warnings


warnings.filterwarnings("ignore")


def send_ppt(event, context):
    if in_production:
        print("In production")
        pubsub_msg = base64.b64decode(event['data']).decode('utf-8')
        json_data = json.loads(pubsub_msg)
        period = json_data['period']
        account = json_data['account']
        project_id = json_data['project_id']
        location = json_data['location']

        print(f"period - {period} account - {account} project_id - {project_id} location - {location}")

    else:
        print("Not in production")

        # period = 'hourly'
        period = 'daily'
        # period = 'weekly'

        # account = 'Athletic Greens'
        account = 'Grubbly Farms'
        # account = 'Caldera'
        # account = 'Pointstory'

        # project_id = 'watchdog-307206'
        project_id = 'grubbly-watchdog'
        # project_id = 'caldera-labs'
        # project_id = 'pointstory'

        location = 'wdt2'
        # location = 'watchdog-test'


    # send_data_recency_alerts(project_id, account, location)
    ppt, negative_warning_count, negative_critical_count, total_count = create_ppt(project_id, account, period)

    if total_count == 0:
        message = "No Alerts "

    elif any([negative_critical_count, negative_warning_count]):
        message = "‼️ "
        if negative_critical_count:
            message = message + f" {negative_critical_count} {'Critical alert' if negative_critical_count == 1 else 'Critical alerts'}"
        if negative_warning_count:
            message = message + f" {negative_warning_count} {'Warning alert' if negative_warning_count == 1 else 'Warning alerts'}"
    else:
        message = f"{total_count} {'Positive alert' if total_count == 1 else 'Positive alerts'}"

    if period == 'daily':
        filepath = f"Anomaly alerts for {yesterday.strftime('%d-%m-%y')}.pptx"
        message = message + f" identified on {yesterday.strftime('%d-%m-%y')}"

    elif period == 'weekly':
        week_start, _ = get_previous_week_start_date_end_date()
        filepath = f"Anomaly alerts for Week {week_start.strftime('%U')}.pptx"
        message = message + f" identified on Week {week_start.strftime('%U')}"
    else:
        raise ValueError(f'Invalid period - {period}')

    if in_production:
        filepath = f"/tmp/{filepath}"
    ppt.save(filepath)
    print(f"Saved {filepath}")
    if total_count > 0:
        send_ppt_to_slack(filepath, message, location)
    else:
        send_ppt_to_slack(None, message, location)


if not in_production:
    send_ppt(None, None)
