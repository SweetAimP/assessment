import pandas as pd
from dataClass import Book
from connection import get_connection
def _get_canceled_item_list():
    conn = get_connection()
    df = pd.read_sql_query('select count(*) from "graded_products"',con=conn)
    return df

def get_item_list():
    active_items = [
        {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    ]
    return active_items

def get_item(item):
    return f"Getting Item {item}"

def get_canceled_res(canceled_item):
    canceled_res = {
            "id": 0,
            "status" : "",
            "metadata" : {
                "last_update" : ""
            }
        }
    canceled_res['id'] = canceled_item['id']
    canceled_res['status'] = canceled_item['status']
    canceled_res['metadata']['last_update'] = canceled_item['last_update']
    return canceled_res