from flask_app.repository import _get_canceled_item_list
from flask_app.summary import SuccessSummary, CancelSummary

def get_canceled_item_list():
    product, metadata = _get_canceled_item_list()
    if product.status == 'cancelled':
        return CancelSummary(product, metadata).serialize()
    elif product.status == 'shipped':
        return SuccessSummary(product, metadata).serialize()
    else:
        pass