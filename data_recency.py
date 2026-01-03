from bigquery import get_bigquery_client
from send_ppt import send_text_to_slack


def send_data_recency_alerts(project_id, account, location):
    print(f"\n\nGetting data recency for {account}")

    client = get_bigquery_client(project_id=project_id)

    query = f"SELECT * FROM `{project_id}.watchdog_data_recency.data_recency`"

    try:
        recency_df = (
            client.query(query)
                .result()
                .to_dataframe()
        )
    except Exception as e:
        return

    not_updated_df = recency_df[~recency_df['is_updated']]

    if not_updated_df.empty:
        print("All source tables are updated")

    else:
        for i, row in not_updated_df.iterrows():
            msg = f"{row['project_id']}.{row['dataset_id']}.{row['table_id']} has not been updated since {row['hours_since_update']} hours"
            send_text_to_slack(msg, location)
        print("Some tables were not updated. Sent data recency alerts")
