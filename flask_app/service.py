from repository import _get_canceled_item_list
from summary import SuccessSummary, CancelSummary

def get_canceled_item_list(license_plate):
    print("Service")
    product, metadata = _get_canceled_item_list(license_plate)
    if product.status == 'cancelled':
        print("Service Cancelled")
        return CancelSummary(product, metadata).serialize()
    elif product.status == 'shipped':
        print("Service Shipped")
        return SuccessSummary(product, metadata).serialize()
    else:
        pass