import tkinter as tk


class TotalsPanel(tk.LabelFrame):

    def __init__(self, parent, calculate_totals_callback):
        super().__init__(
            parent,
            text="Bill Summary",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            width=260,
        )

        self._calculate_totals_callback = calculate_totals_callback
        self.bill_no_var = tk.StringVar(value="QB-000001")
        self.subtotal_var = tk.StringVar(value="₹ 0.00")
        self.tax_var = tk.StringVar(value="₹ 0.00")
        self.discount_var = tk.StringVar(value="₹ 0.00")
        self.total_var = tk.StringVar(value="₹ 0.00")

        self._build_rows()

    def _build_rows(self):
        labels = [
            ("Bill No.", self.bill_no_var),
            ("Subtotal", self.subtotal_var),
            ("GST", self.tax_var),
            ("Discount", self.discount_var),
            ("Grand Total", self.total_var),
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

    def set_bill_number(self, bill_no):

        self.bill_no_var.set(bill_no)

    def refresh_totals(self):
        subtotal, tax, discount, total = self._calculate_totals_callback()

        self.subtotal_var.set(f"₹ {subtotal:.2f}")
        self.tax_var.set(f"₹ {tax:.2f}")
        self.discount_var.set(f"₹ {discount:.2f}")
        self.total_var.set(f"₹ {total:.2f}")

    def set_totals(self, subtotal, tax, discount, total):
        self.subtotal_var.set(f"₹ {subtotal:.2f}")
        self.tax_var.set(f"₹ {tax:.2f}")
        self.discount_var.set(f"₹ {discount:.2f}")
        self.total_var.set(f"₹ {total:.2f}")
