from logic.cart import cart
from logic.config import get as get_config


class AppState:

    def __init__(self):

        self.cart = cart

        self.current_customer = {
            "name": "Walk-in Customer",
            "mobile": "",
            "address": "",
            "gst": ""
        }

        self.current_product = None

        self.invoice_no = ""

        self.total = 0

        self.status = "Ready"

        self.scanner_connected = False

        self.scanner_mode = "mobile_camera"

        self.operator = get_config("company", "cashier_name", "Admin")

        self.hold_bills = []


app_state = AppState()