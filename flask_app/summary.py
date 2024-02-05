class Summary():
    def __init__(self, product, metadata):
        self.product = product
        self.metadata = metadata
    
    def serialize(self):
        summary = {
            "product" : {},
            "metadata": {}
            }
        product_vars = vars(self.product)
        metadata_vars = vars(self.metadata)
        for p_attr in self.p_attr:
            summary["product"][p_attr] = product_vars[p_attr]
        for m_attr in self.m_attr:
            summary["metadata"][m_attr] = metadata_vars[m_attr]
        return summary


class CancelSummary(Summary):
    def __init__(self, product, metada):
        super().__init__(product, metada)
        self.p_attr = [
            "license_plate",
            "status"
        ]
        self.m_attr = [
            "last_update"
        ]

class SuccessSummary(Summary):
    def __init__(self, product, metada):
        super().__init__(product, metada)
        self.p_attr = [
            "license_plate",
            "sold_price",
            "buybay_fee",
            "transport_cost",
            "platform_fee",
            "grading_fee",
            "partner_payout",
        ]
        self.m_attr = [
            "last_update"
        ]