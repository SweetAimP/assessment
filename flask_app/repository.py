import pandas as pd
from dataClass import Product,Metadata
from connection import get_connection

def set_product(df):
    return Product (
        
    )

def set_metadata(df):
    return  Metadata(
        df['last_update'].iloc[0]
    )


def _get_canceled_item_list(license_plate):
    query = "select * from sold_products where lincense_plate = '{}'".format(license_plate)
    df = pd.read_sql_query(query,con=get_connection())
    if df.empty:
        return Product(), Metadata()
    else:
        return set_product(df), set_metadata(df)           