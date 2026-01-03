import os
from collections import defaultdict


WATCHDOG_PROJECT_ID = 'watchdog-307206'

TEST_WEBHOOK = os.getenv('TEAMS_WEBHOOK_URL', 'replace_teams_webhook')

AG_WEBHOOK = os.getenv('AG_TEAMS_WEBHOOK_URL', 'replace_ag_teams_webhook')

REVERSE_METRICS = [
    'bounce_rate',
    'ship_time',
    'click_to_delivery_time',
    'cancelled_subscriptions',
    'cpc',
    'orders_returned',
    'refund_amount',
    'acos',
]

in_production = os.getenv('GCP_PROJECT')


class Kpi:
    def __init__(self, data_source, dimension, dim_label, metric):
        self.data_source = data_source
        self.dimension = dimension
        self.dim_label = dim_label
        self.metric = metric
        self.xaxis_data = None
        self.yaxis_data = None


default_kpi_list = [
        Kpi('Ecommerce', None, None, 'Revenue'),
        Kpi('Google Analytics', None, None, 'Traffic'),
        Kpi('Google Analytics', None, None, 'Conversion_Rate'),
        Kpi('Ecommerce', None, None, 'AOV'),
]

kpi_list_dict = defaultdict(lambda: default_kpi_list)

kpi_list_dict['Athletic Greens'] = [
        Kpi('Ecommerce', None, None, 'Revenue'),
        Kpi('Google Analytics', None, None, 'Traffic'),
        Kpi('Google Analytics', None, None, 'Conversion_Rate'),
        Kpi('Ecommerce', None, None, 'New_Subscriptions'),
        Kpi('Ecommerce', None, None, 'Take_Rate'),
        # Kpi('Ecommerce', None, None, 'Cancelled_Subscriptions'),
        Kpi('Ecommerce', None, None, 'Total_Subscribers'),
]

kpi_list_dict['Grubbly Farms'] = [
        Kpi('Ecommerce', None, None, 'Gross_Revenue'),
        Kpi('Ecommerce', None, None, 'Orders'),
        Kpi('Ecommerce', None, None, 'New_Customers'),
        Kpi('Google Analytics', None, None, 'Sessions'),
        Kpi('Ecommerce', None, None, 'AOV'),
        Kpi('Ecommerce', None, None, 'CAC_Shopify'),
]

kpi_list_dict['Caldera'] = [
        Kpi('Ecommerce', None, None, 'Revenue_A'),
        Kpi('Ecommerce', None, None, 'Total_Orders'),
        Kpi('Ecommerce', None, None, 'AOV_A'),
        Kpi('Ecommerce', None, None, 'New_Customers_Added'),
        Kpi('Google Analytics', None, None, 'Traffic'),
        Kpi('Google Analytics', None, None, 'Conversion_Rate'),
]

kpi_list_dict['Pointstory'] = [
        Kpi('Ecommerce', None, None, 'Total_Sales'),
        Kpi('Google Analytics', None, None, 'Traffic'),
        Kpi('Google Analytics', None, None, 'Conversion_Rate'),
        Kpi('Ecommerce', None, None, 'AOV'),
]
