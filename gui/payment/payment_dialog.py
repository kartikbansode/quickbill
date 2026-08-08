import tkinter as tk
from tkinter import messagebox, ttk


class PaymentDialog(tk.Toplevel):

    def __init__(
        self,
        parent,
        total_amount,
        on_complete,
        on_payment_start=None,
        on_payment_cancel=None,
    ):
        super().__init__(parent)

        self.title("Complete Sale")
        self.geometry("520x560")
        self.resizable(False, False)

        self.total = float(total_amount)
        self.on_complete = on_complete
        self.on_payment_start = on_payment_start
        self.on_payment_cancel = on_payment_cancel

        self.payment_mode = tk.StringVar(value="Cash")

        self.received = tk.StringVar(value=f"{self.total:.2f}")

        self.balance = tk.StringVar(value="₹ 0.00")

        self.status = tk.StringVar(value="Ready")

        self.complete_button = None

        self.build_ui()

        self.received.trace_add("write", lambda *args: self.calculate_balance())

        self.calculate_balance()

        self.grab_set()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancel_payment,
        )

        self.bind(
            "<Escape>",
            lambda event: self.cancel_payment(),
        )

    # =========================================================
    # UI
    # =========================================================

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
            text=f"Grand Total\n₹ {self.total:,.2f}",
            font=("Segoe UI", 20, "bold"),
            fg="#0a7d32",
            bg="white",
        ).pack(pady=(0, 12))

        # -----------------------------------------------------
        # Payment Method
        # -----------------------------------------------------

        method_frame = tk.LabelFrame(
            self,
            text="Payment Method",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )

        method_frame.pack(
            fill="x",
            padx=20,
            pady=5,
        )

        methods = (
            ("Cash", "Cash"),
            ("UPI", "UPI"),
            ("Card", "Card"),
            ("Credit", "Credit"),
        )

        for text, value in methods:

            ttk.Radiobutton(
                method_frame,
                text=text,
                variable=self.payment_mode,
                value=value,
                command=self.payment_mode_changed,
            ).pack(
                side="left",
                padx=12,
                pady=8,
            )

        # -----------------------------------------------------
        # Dynamic Payment Area
        # -----------------------------------------------------

        self.payment_area = tk.Frame(
            self,
            bg="white",
        )

        self.payment_area.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10,
        )

        self.build_cash_payment()

        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        self.status_label = tk.Label(
            self,
            textvariable=self.status,
            bg="white",
            fg="#555555",
            font=("Segoe UI", 9),
        )

        self.status_label.pack(pady=(0, 5))

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        button_frame = tk.Frame(
            self,
            bg="white",
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=15,
        )

        self.complete_button = tk.Button(
            button_frame,
            text="Complete Sale",
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            command=self.complete_sale,
            relief="flat",
            height=2,
        )

        self.complete_button.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 5),
        )

        self.update_complete_button()

        tk.Button(
            button_frame,
            text="Cancel",
            bg="#dc3545",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            command=self.cancel_payment,
            relief="flat",
            height=2,
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(5, 0),
        )

    # =========================================================
    # CLEAR PAYMENT AREA
    # =========================================================

    def clear_payment_area(self):

        for widget in self.payment_area.winfo_children():

            widget.destroy()

    def notify_payment_start(self):

        callback = self.on_payment_start

        if callback is None:
            return

        try:

            callback(
                self.payment_mode.get(),
                self.total,
            )

        except Exception as exc:

            print(
                f"[CustomerDisplay] Payment start notification failed: {exc}"
            )

    # =========================================================
    # PAYMENT MODE
    # =========================================================

    def payment_mode_changed(self):

        mode = self.payment_mode.get()

        # Notify the optional customer display.
        self.notify_payment_start()

        self.clear_payment_area()

        if mode == "Cash":

            self.build_cash_payment()

        elif mode == "UPI":

            self.build_upi_payment()

        elif mode == "Card":

            self.build_card_payment()

        elif mode == "Credit":

            self.build_credit_payment()

        self.update_complete_button()

    # =========================================================
    # CASH
    # =========================================================

    def build_cash_payment(self):

        self.status.set("Enter the amount received from the customer.")

        tk.Label(
            self.payment_area,
            text="Received Amount",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        self.received_entry = tk.Entry(
            self.payment_area,
            textvariable=self.received,
            font=("Segoe UI", 14),
            justify="right",
        )

        self.received_entry.pack(
            fill="x",
            pady=(4, 15),
        )

        self.received_entry.focus_set()

        self.received_entry.select_range(
            0,
            tk.END,
        )

        tk.Label(
            self.payment_area,
            text="Change / Balance",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        self.balance_label = tk.Label(
            self.payment_area,
            textvariable=self.balance,
            bg="#eff6ff",
            fg="#2563eb",
            font=("Segoe UI", 20, "bold"),
            anchor="e",
            padx=10,
            pady=10,
        )

        self.balance_label.pack(
            fill="x",
            pady=(4, 10),
        )

        self.calculate_balance()

    # =========================================================
    # UPI
    # =========================================================

    def build_upi_payment(self):

        self.status.set("UPI payment selected.")

        tk.Label(
            self.payment_area,
            text="UPI PAYMENT",
            bg="white",
            fg="#2563eb",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(15, 8))

        tk.Label(
            self.payment_area,
            text=f"Amount to Pay\n₹ {self.total:,.2f}",
            bg="#eff6ff",
            fg="#1e3a8a",
            font=("Segoe UI", 16, "bold"),
            pady=15,
        ).pack(
            fill="x",
            pady=5,
        )

        self.qr_placeholder = tk.Frame(
            self.payment_area,
            bg="#f8fafc",
            height=150,
            width=150,
            highlightbackground="#d1d5db",
            highlightthickness=1,
        )

        self.qr_placeholder.pack(pady=15)

        self.qr_placeholder.pack_propagate(False)

        tk.Label(
            self.qr_placeholder,
            text="UPI QR\n\nWill be generated\nhere",
            bg="#f8fafc",
            fg="#6b7280",
            font=("Segoe UI", 10),
            justify="center",
        ).pack(expand=True)

        tk.Label(
            self.payment_area,
            text="QR generation will be connected after\nmerchant UPI settings are added.",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 9),
            justify="center",
        ).pack(pady=5)

        self.upi_paid_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            self.payment_area,
            text="Payment received",
            variable=self.upi_paid_var,
            command=self.update_complete_button,
        ).pack(pady=5)

    # =========================================================
    # CARD
    # =========================================================

    def build_card_payment(self):

        self.status.set("Collect ₹ " f"{self.total:,.2f} " "using the card machine.")

        tk.Label(
            self.payment_area,
            text="CARD PAYMENT",
            bg="white",
            fg="#7c3aed",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(25, 10))

        tk.Label(
            self.payment_area,
            text=f"Amount\n₹ {self.total:,.2f}",
            bg="#f5f3ff",
            fg="#5b21b6",
            font=("Segoe UI", 18, "bold"),
            pady=20,
        ).pack(
            fill="x",
            pady=10,
        )

        self.card_paid_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            self.payment_area,
            text="Card payment received",
            variable=self.card_paid_var,
            command=self.update_complete_button,
        ).pack(pady=15)

    # =========================================================
    # CREDIT
    # =========================================================

    def build_credit_payment(self):

        self.status.set("This sale will be recorded as credit.")

        tk.Label(
            self.payment_area,
            text="CREDIT SALE",
            bg="white",
            fg="#d97706",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(25, 10))

        tk.Label(
            self.payment_area,
            text=f"Credit Amount\n₹ {self.total:,.2f}",
            bg="#fffbeb",
            fg="#92400e",
            font=("Segoe UI", 18, "bold"),
            pady=20,
        ).pack(
            fill="x",
            pady=10,
        )

        tk.Label(
            self.payment_area,
            text="Customer credit will be recorded.\n"
            "Customer management can be connected later.",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 9),
            justify="center",
        ).pack(pady=10)

        self.credit_confirm_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            self.payment_area,
            text="Confirm credit sale",
            variable=self.credit_confirm_var,
            command=self.update_complete_button,
        ).pack(pady=10)

    # =========================================================
    # CASH CALCULATION
    # =========================================================

    def calculate_balance(self):

        if self.payment_mode.get() != "Cash":

            return

        try:

            received = float(self.received.get())

        except (
            TypeError,
            ValueError,
        ):

            received = 0.0

        balance = received - self.total

        self.balance.set(f"₹ {balance:,.2f}")

        self.update_complete_button()

    # =========================================================
    # BUTTON STATE
    # =========================================================

    def update_complete_button(self):

        # The payment UI is built before the bottom buttons.
        # During initial construction the button does not exist yet.

        if self.complete_button is None:
            return

        mode = self.payment_mode.get()

        enabled = True

        if mode == "Cash":

            try:
                received = float(self.received.get())

                enabled = received >= self.total

            except (
                TypeError,
                ValueError,
            ):

                enabled = False

        elif mode == "UPI":

            enabled = hasattr(self, "upi_paid_var") and self.upi_paid_var.get()

        elif mode == "Card":

            enabled = hasattr(self, "card_paid_var") and self.card_paid_var.get()

        elif mode == "Credit":

            enabled = (
                hasattr(self, "credit_confirm_var") and self.credit_confirm_var.get()
            )

        self.complete_button.config(state="normal" if enabled else "disabled")

    # =========================================================
    # COMPLETE SALE
    # =========================================================

    def complete_sale(self):

        mode = self.payment_mode.get()

        # -----------------------------------------------------
        # Cash
        # -----------------------------------------------------

        if mode == "Cash":

            try:

                received = float(self.received.get())

            except (
                TypeError,
                ValueError,
            ):

                messagebox.showerror(
                    "Invalid Amount",
                    "Please enter a valid received amount.",
                    parent=self,
                )

                return

            if received < self.total:

                messagebox.showwarning(
                    "Insufficient Amount",
                    (
                        f"Received amount is ₹ {received:,.2f}.\n\n"
                        f"Required amount is ₹ {self.total:,.2f}."
                    ),
                    parent=self,
                )

                return

        else:

            received = self.total

        # -----------------------------------------------------
        # UPI
        # -----------------------------------------------------

        if mode == "UPI":

            if not self.upi_paid_var.get():

                return

        # -----------------------------------------------------
        # Card
        # -----------------------------------------------------

        if mode == "Card":

            if not self.card_paid_var.get():

                return

        # -----------------------------------------------------
        # Credit
        # -----------------------------------------------------

        if mode == "Credit":

            if not self.credit_confirm_var.get():

                return

        self.status.set("Completing sale...")

        self.complete_button.config(state="disabled")

        self.update_idletasks()

        try:

            self.on_complete(
                mode,
                received,
            )

        except Exception:

            self.complete_button.config(state="normal")

            raise

        self.destroy()

    # =========================================================
    # CANCEL
    # =========================================================

    def cancel_payment(self):

        callback = self.on_payment_cancel

        if callback is not None:

            try:

                callback(
                    self.payment_mode.get()
                )

            except Exception as exc:

                print(
                    f"[CustomerDisplay] Payment cancel notification failed: {exc}"
                )

        self.destroy()