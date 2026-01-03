from pptx import Presentation
from pptx.util import Inches
from bigquery import get_bigquery_client
from data import get_asset_df
from kpi_slide import add_kpi_slide
from anomaly_slide import add_anomaly_slide
from rca_slide import add_rca_slide
from config import kpi_list_dict


BASE_FONT_SIZE = 18


def new_ppt():
    ppt = Presentation()
    ppt.slide_width = Inches(13.33)
    ppt.slide_height = Inches(7.5)

    return ppt


def get_anomaly_type_counts(asset_df):
    negative_mask = asset_df['yhat_color'] == 'red'
    warning_mask = asset_df['is_warning']
    critical_mask = asset_df['is_critical']

    negative_warning_count = asset_df[negative_mask & warning_mask].shape[0]
    negative_critical_count = asset_df[negative_mask & critical_mask].shape[0]

    return negative_warning_count, negative_critical_count


def add_asset_slides(ppt, account, project_id, dataset_id, asset, period):
    print(f"\n\nGetting data for {asset}...")
    asset_df, errors = get_asset_df(account, project_id, dataset_id, period)
    if asset_df.empty:
        print(f"asset_df is empty for {account} {asset}")
        return 0, 0, 0

    print(f"Got data for {asset}")

    kpi_list = kpi_list_dict[account]
    if period == 'weekly':
        add_kpi_slide(ppt, period, asset, asset_df, kpi_list)

    negative_warning_count = 0
    negative_critical_count = 0
    total_count = 0

    if not (account == 'Athletic Greens' and asset == 'Overall'):
    # if True:
        print(f"\n\nPreparing anomaly slide for {asset}...")
        w, c, t = add_anomaly_slide(ppt, period, asset, asset_df, kpi_list)
        negative_warning_count += w
        negative_critical_count += c
        total_count += t
        # add_rca_slide(ppt, period, asset_df)

    return negative_warning_count, negative_critical_count, total_count


def create_ppt(project_id, account, period):
    ppt = new_ppt()

    # add_asset_slides(ppt, account, project_id, dataset_id='Overall', asset='Overall', period=period)
    # add_asset_slides(ppt, account, project_id, dataset_id='AG_USA', asset='AG_USA', period=period)
    # add_asset_slides(ppt, account, project_id, dataset_id='AG_EU', asset='AG_EU', period=period)
    # add_asset_slides(ppt, account, project_id, dataset_id='AG_UK', asset='AG_UK', period=period)

    client = get_bigquery_client(project_id='watchdog-307206')

    query = f"SELECT * FROM `watchdog-307206.config.account_assets` WHERE account = '{account}' ORDER BY sequence_no"
    dataset_df = (
        client.query(query)
            .result()
            .to_dataframe()
    )

    print("Got list of assets")

    negative_warning_count = 0
    negative_critical_count = 0
    total_count = 0

    for i, row in dataset_df.iterrows():
        w, c, t = add_asset_slides(ppt, account, project_id, dataset_id=row['dataset_id'], asset=row['asset'], period=period)
        negative_warning_count += w
        negative_critical_count += c
        total_count += t

    return ppt, negative_warning_count, negative_critical_count, total_count
