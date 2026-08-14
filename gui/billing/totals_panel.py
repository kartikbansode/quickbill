import tkinter as tk
from logic.config import get_currency


class TotalsPanel(tk.Frame):

    def __init__(self, parent, calculate_totals_callback):
        super().__init__(
            parent,
            bg="white",
            width=260,
        )

        self._calculate_totals_callback = calculate_totals_callback
        self.bill_no_var = tk.StringVar(value="QB-000001")
        self.subtotal_var = tk.StringVar(value=f"{get_currency()} 0.00")
        self.tax_var = tk.StringVar(value=f"{get_currency()} 0.00")
        self.discount_var = tk.StringVar(value=f"{get_currency()} 0.00")
        self.total_var = tk.StringVar(value=f"{get_currency()} 0.00")

        self._build_rows()

    def _build_rows(self):
        labels = [
            ("Subtotal", self.subtotal_var),
            ("GST", self.tax_var),
            ("Discount", self.discount_var),
        ]

        for text, var in labels:

            row = tk.Frame(self, bg="white")

            row.pack(fill="x", padx=10, pady=3)

            tk.Label(
                row, text=text, bg="white", width=12, anchor="w", font=("Segoe UI", 10)
            ).pack(side="left")

            tk.Label(
                row,
                textvariable=var,
                bg="white",
                fg="#1d3557",
                font=("Segoe UI", 11, "bold"),
            ).pack(side="right")

            # Divider
        tk.Frame(
            self,
            bg="#d0d0d0",
            height=2,
        ).pack(fill="x", padx=8, pady=8)

        # Grand Total
        grand_frame = tk.Frame(self, bg="#e8f5e9")
        grand_frame.pack(fill="x", padx=8, pady=5)

        tk.Label(
            grand_frame,
            text="GRAND TOTAL",
            bg="#e8f5e9",
            fg="#006400",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=8, pady=(5,0))

        tk.Label(
            grand_frame,
            textvariable=self.total_var,
            bg="#e8f5e9",
            fg="#008000",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="e", padx=8, pady=(0,5))

    def set_bill_number(self, bill_no):

        self.bill_no_var.set(bill_no)

    def refresh_totals(self):
        subtotal, tax, discount, total = self._calculate_totals_callback()

        self.subtotal_var.set(f"{get_currency()} {subtotal:.2f}")
        self.tax_var.set(f"{get_currency()} {tax:.2f}")
        self.discount_var.set(f"{get_currency()} {discount:.2f}")
        self.total_var.set(f"{get_currency()} {total:.2f}")

    def set_totals(self, subtotal, tax, discount, total):
        self.subtotal_var.set(f"{get_currency()} {subtotal:.2f}")
        self.tax_var.set(f"{get_currency()} {tax:.2f}")
        self.discount_var.set(f"{get_currency()} {discount:.2f}")
        self.total_var.set(f"{get_currency()} {total:.2f}")
