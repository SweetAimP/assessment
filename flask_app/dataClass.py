
class Product():
    def __init__(self, license_plate, sold_price, buybay_fee, transport_cost, platform_fee, grading_fee, partner_payout) -> None:
        self.license_plate = license_plate
        self.sold_price = sold_price
        self.buybay_fee = buybay_fee
        self.transport_cost = transport_cost
        self.platform_fee = platform_fee
        self.grading_fee = grading_fee
        self.partner_payout = partner_payout



class Metadata():
    def __init__(self, last_update) -> None:
        self.last_update = last_update