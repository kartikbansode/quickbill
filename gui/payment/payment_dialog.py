import tkinter as tk
from tkinter import ttk


class PaymentDialog(tk.Toplevel):

    def __init__(self, parent, total_amount, on_complete):
        super().__init__(parent)

        self.title("Complete Sale")
        self.geometry("520x520")
        self.resizable(False, False)

        self.total = total_amount
        self.on_complete = on_complete

        self.payment_mode = tk.StringVar(value="Cash")
        self.received = tk.StringVar(value=f"{total_amount:.2f}")
        self.balance = tk.StringVar(value="₹ 0.00")

        self.build_ui()

        self.received.trace_add("write", lambda *args: self.calculate_balance())

        self.calculate_balance()

        self.grab_set()

        self.bind("<Return>", lambda event: self.complete_sale())

    def build_ui(self):

        self.configure(bg="white")

        tk.Label(
            self,
            text="Complete Sale",
            font=("Segoe UI", 16, "bold"),
            bg="white",
        ).pack(pady=(15, 5))

        tk.Label(
            self,
            text=f"Grand Total\n₹ {self.total:.2f}",
            font=("Segoe UI", 20, "bold"),
            fg="#0a7d32",
            bg="white",
        ).pack(pady=(0, 10))

        frame = tk.LabelFrame(
            self,
            text="Payment Method",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )
        frame.pack(fill="x", padx=20, pady=5)

        for mode in ("Cash", "UPI", "Card", "Credit"):

            ttk.Radiobutton(
                frame,
                text=mode,
                variable=self.payment_mode,
                value=mode,
            ).pack(anchor="w", padx=10, pady=2)

        body = tk.Frame(self, bg="white")
        body.pack(fill="x", padx=20, pady=10)

        tk.Label(
            body,
            text="Received Amount",
            bg="white",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        self.received_entry = tk.Entry(
            body,
            textvariable=self.received,
            font=("Segoe UI", 12),
        )

        self.received_entry.pack(fill="x", pady=(2, 10))

        self.received_entry.focus_set()
        self.received_entry.select_range(0, tk.END)

        tk.Label(
            body,
            text="Balance",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        tk.Label(
            body,
            textvariable=self.balance,
            bg="white",
            fg="#2563eb",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", pady=(2, 10))

        # ---------------- Buttons ----------------

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(side="bottom", fill="x", padx=20, pady=15)

        tk.Button(
            button_frame,
            text="Complete Sale",
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            command=self.complete_sale,
            relief="flat",
            height=2,
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        tk.Button(
            button_frame,
            text="Cancel",
            bg="#dc3545",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            command=self.destroy,
            relief="flat",
            height=2,
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

    def calculate_balance(self):

        try:

            received = float(self.received.get())

        except:

            received = 0

        balance = received - self.total

        self.balance.set(f"₹ {balance:.2f}")

    def complete_sale(self):

        try:

            received = float(self.received.get())

        except:

            return

        self.withdraw()

        self.on_complete(
            self.payment_mode.get(),
            received,
        )

        self.destroy()
