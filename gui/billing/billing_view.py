import tkinter as tk

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

        # Use a container with grid layout to manage sections
        billing_container = tk.Frame(self, bg="#e9ecef")
        billing_container.grid(row=0, column=0, sticky="nsew", padx=8, pady=5)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Row 0: Scanner panel (fixed height)
        self.scanner_panel = ScannerPanel(billing_container)
        self.scanner_panel.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=5)
        self.scanner_panel.set_scan_callbacks(
            self.callbacks.get("start_scan"),
            self.callbacks.get("stop_scan"),
        )
        self.scanner_panel.add_button.config(command=self._handle_manual_barcode)

        # Row 1: Table frame (expands)
        table_frame = tk.LabelFrame(
            billing_container,
            text="Current Bill",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(2, 8))
        billing_container.grid_rowconfigure(1, weight=1)
        billing_container.grid_columnconfigure(0, weight=1)

        self.cart_table = CartTable(table_frame)
        self.cart_table.pack(fill="both", expand=True)

        self.cart_table.set_actions(
            self.callbacks.get("increase_qty"),
            self.callbacks.get("decrease_qty"),
            self.callbacks.get("delete_item"),
        )

        # Row 2: Bottom panel (fixed height) containing quick actions and bill summary
        bottom_panel = tk.Frame(billing_container, bg="#e9ecef")
        bottom_panel.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(2, 0))

        left_panel = tk.LabelFrame(
            bottom_panel,
            text="Quick Actions",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )

        left_panel.pack(side="left", fill="both", expand=True)

        button_width = 13

        tk.Button(
            left_panel,
            text="🆕 New Bill",
            width=button_width,
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=self.callbacks.get("clear_cart"),
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            left_panel,
            text="📋 Hold",
            width=button_width,
            bg="#8e44ad",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=self.callbacks.get("hold_bill"),
        ).grid(row=1, column=1, padx=5, pady=5)

        self.generate_button = tk.Button(
            left_panel,
            text="🧾 Generate",
            width=button_width,
            bg="#16a085",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            command=self.callbacks.get("generate_bill"),
            state="disabled",
        )
        self.generate_button.grid(row=1, column=2, padx=5, pady=5)

        right_panel = tk.LabelFrame(
            bottom_panel,
            text="Bill Summary",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            width=260,
        )

        right_panel.pack(side="right", fill="y", padx=5)

        self.totals_panel = TotalsPanel(
            right_panel,
            self.callbacks.get("calculate_totals", lambda: (0, 0, 0, 0)),
        )
        self.totals_panel.pack(fill="both", expand=True, padx=0, pady=0)

    def _handle_manual_barcode(self):
        barcode = self.get_manual_barcode()
        if not barcode:
            return

        callback = self.callbacks.get("barcode")
        if callback:
            callback(barcode)

        self.clear_manual_barcode()
        self.focus_manual_barcode()

    def render_cart(self, items):
        self.cart_table.refresh_table(items)
        self.totals_panel.refresh_totals()
        
        if items:
            self.generate_button.config(state="normal", bg="#16a085")
        else:
            self.generate_button.config(state="disabled", bg="#95a5a6")

    def refresh_totals(self):
        self.totals_panel.refresh_totals()

    def set_bill_number(self, bill_no):

        self.totals_panel.set_bill_number(bill_no)

    def get_manual_barcode(self):
        return self.scanner_panel.get_barcode()

    def clear_manual_barcode(self):
        self.scanner_panel.clear()

    def focus_manual_barcode(self):
        self.scanner_panel.focus()

    def update_scanner_status(self, text):
        self.scanner_panel.update_status(text)

    def display_product(self, product):
        self.scanner_panel.display_product(product)

    def toggle_scan(self):
        self.scanner_panel.toggle_scan()
