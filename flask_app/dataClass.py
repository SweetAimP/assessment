
class Product():
    def __init__(self, license_plate=None, sold_price=None, buybay_fee=None, transport_cost=None, platform_fee=None, grading_fee=None, partner_payout=None) -> None:
        self.license_plate = license_plate
        self.sold_price = sold_price
        self.buybay_fee = buybay_fee
        self.transport_cost = transport_cost
        self.platform_fee = platform_fee
        self.grading_fee = grading_fee
        self.partner_payout = partner_payout

class Metadata():
    def __init__(self, last_update=None) -> None:
        self.last_update = last_update