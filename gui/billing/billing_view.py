import tkinter as tk
from gui.ui_components import set_button_state, create_success_button

from gui.billing.cart_table import CartTable
from gui.billing.scanner_panel import ScannerPanel
from gui.billing.totals_panel import TotalsPanel


class BillingView(tk.Frame):

    def __init__(self, parent, callbacks):

        super().__init__(parent, bg="#e9ecef")

        self.callbacks = callbacks
        self.scanner_panel = None
        self.cart_table = None
        self.totals_panel = None
        self.generate_button = None

        self.build_ui()

    def build_ui(self):

        billing_container = tk.Frame(self, bg="#e9ecef")
        billing_container.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=8,
            pady=5
        )

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ---------------------------------------------------------
        # ROW 0: PRODUCT SCANNER
        # ---------------------------------------------------------

        self.scanner_panel = ScannerPanel(billing_container)
        self.scanner_panel.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=0,
            pady=5
        )

        self.scanner_panel.set_scan_callbacks(
            self.callbacks.get("start_scan"),
            self.callbacks.get("stop_scan"),
        )

        self.scanner_panel.add_button.config(
            command=self._handle_manual_barcode
        )

        # ---------------------------------------------------------
        # ROW 1: CURRENT BILL / CART
        # ---------------------------------------------------------

        table_frame = tk.LabelFrame(
            billing_container,
            text="Current Bill",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )

        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(2, 5)
        )

        billing_container.grid_rowconfigure(1, weight=1)
        billing_container.grid_columnconfigure(0, weight=1)

        self.cart_table = CartTable(table_frame)
        self.cart_table.pack(
            fill="both",
            expand=True
        )

        self.cart_table.set_actions(
            self.callbacks.get("increase_qty"),
            self.callbacks.get("decrease_qty"),
            self.callbacks.get("delete_item"),
        )

        # ---------------------------------------------------------
        # ROW 2: BOTTOM PANEL ( Actions + Totals)
        # ---------------------------------------------------------

        bottom_panel = tk.Frame(billing_container, bg="#e9ecef")
        bottom_panel.grid(row=2, column=0, sticky="ew", pady=(0, 2))
        
        bottom_panel.grid_columnconfigure(0, weight=1)
        bottom_panel.grid_columnconfigure(1, weight=0)

        # Actions (Left)
        quick_actions_frame = tk.LabelFrame(
            bottom_panel,
            text="Actions",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )
        quick_actions_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        self.generate_button = create_success_button(
            quick_actions_frame,
            "🧾 Generate Bill (F4)",
            command=self.callbacks.get("generate_bill"),
            width=22,
            state="disabled"
        )
        self.generate_button.pack(side="left", padx=15, pady=10)

        # Bill Summary / Totals (Right)
        summary_frame = tk.LabelFrame(
            bottom_panel,
            text="Bill Summary",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )
        summary_frame.grid(row=0, column=1, sticky="nsew")

        self.totals_panel = TotalsPanel(
            summary_frame,
            self.callbacks.get(
                "calculate_totals",
                lambda: (0, 0, 0, 0)
            ),
        )

        self.totals_panel.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

    # -------------------------------------------------------------
    # BARCODE HANDLING
    # -------------------------------------------------------------

    def _handle_manual_barcode(self):

        barcode = self.get_manual_barcode()

        if not barcode:
            return

        callback = self.callbacks.get("barcode")

        if callback:
            callback(barcode)

        self.clear_manual_barcode()
        self.focus_manual_barcode()

    # -------------------------------------------------------------
    # CART
    # -------------------------------------------------------------

    def render_cart(self, items):

        self.cart_table.refresh_table(items)
        self.totals_panel.refresh_totals()
        
        if self.generate_button:
            if items:
                set_button_state(self.generate_button, "normal")
            else:
                set_button_state(self.generate_button, "disabled")

    # -------------------------------------------------------------
    # TOTALS
    # -------------------------------------------------------------

    def refresh_totals(self):

        self.totals_panel.refresh_totals()

    # -------------------------------------------------------------
    # BILL NUMBER
    # -------------------------------------------------------------

    def set_bill_number(self, bill_no):

        self.totals_panel.set_bill_number(bill_no)

    # -------------------------------------------------------------
    # BARCODE FIELD
    # -------------------------------------------------------------

    def get_manual_barcode(self):

        return self.scanner_panel.get_barcode()

    def clear_manual_barcode(self):

        self.scanner_panel.clear()

    def focus_manual_barcode(self):

        self.scanner_panel.focus()

    # -------------------------------------------------------------
    # SCANNER
    # -------------------------------------------------------------

    def update_scanner_status(self, text):

        self.scanner_panel.update_status(text)

    def display_product(self, product):

        self.scanner_panel.display_product(product)

    def toggle_scan(self):

        self.scanner_panel.toggle_scan()