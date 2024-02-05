from repository import _get_canceled_item_list
from summary import SuccessSummary, CancelSummary

def get_canceled_item_list(license_plate):
    product, metadata = _get_canceled_item_list(license_plate)
    if product.status == 'cancelled':
        return CancelSummary(product, metadata).serialize()
    elif product.status == 'shipped':
        return SuccessSummary(product, metadata).serialize()
    elif  product.status == None:
        return "Record not found"