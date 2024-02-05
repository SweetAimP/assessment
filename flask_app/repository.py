import pandas as pd
from dataClass import Product,Metadata
from connection import get_connection

def set_product(df):
    return Product (
        license_plate=df['license_plate'].iloc[0],
        status=df['status'].iloc[0],
        sold_price=df['sold_price'].iloc[0],
        buybay_fee=df['buybay_fee'].iloc[0],
        transport_fee=df['transport_fee'].iloc[0],
        platform_fee=df['platform_fee'].iloc[0],
        grading_fee=df['grading_fee'].iloc[0],
        partner_payout=df['partner_payout'].iloc[0]
    )

def set_metadata(df):
    return  Metadata(
        last_update = df['last_update'].iloc[0]
    )


def _get_canceled_item_list(license_plate):
    query = "select * from base_records where license_plate = '{}' ;".format(license_plate)
    df = pd.read_sql_query(query,con=get_connection())
    if df.empty:
        return Product(), Metadata()
    else:
        return set_product(df), set_metadata(df)           