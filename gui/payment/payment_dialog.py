import tkinter as tk
from tkinter import ttk
from urllib.parse import quote
from gui.ui_components import show_error, show_warning, show_confirmation, set_button_state, BG_DISABLED, TEXT_DISABLED

try:
    import qrcode
    from PIL import ImageTk

    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


class PaymentDialog(tk.Toplevel):
    """
    QuickBill professional payment dialog.

    Desktop remains the source of truth for the transaction.

    The Customer Display receives the current payment state and,
    for UPI, the exact same UPI QR payload used by this window.
    """

    BG = "#f3f6fa"
    CARD = "#ffffff"
    BORDER = "#d9e1ea"

    TEXT = "#172033"
    MUTED = "#667085"

    PRIMARY = "#2563eb"
    PRIMARY_DARK = "#0f55b7"

    SUCCESS = "#16a34a"
    SUCCESS_DARK = "#166534"
    SUCCESS_BG = "#ecfdf3"

    DANGER = "#dc2626"
    DANGER_BG = "#fef2f2"

    WARNING = "#f59e0b"
    WARNING_BG = "#fffbeb"

    BLUE_BG = "#eff6ff"

    UPI_ID = "8793432136-4@ybl"
    MERCHANT_NAME = "QuickBill"

    PAYMENT_MODES = (
        "Cash",
        "UPI",
        "Card",
        "Credit",
    )

    def __init__(
        self,
        parent,
        total_amount,
        on_complete,
        on_payment_start=None,
        on_payment_cancel=None,
        bill_no="",
    ):
        super().__init__(parent)

        self.parent_window = parent

        try:
            self.total = round(float(total_amount), 2)
            self.bill_no = str(bill_no or "")
        except (TypeError, ValueError):
            self.total = 0.0

        self.bill_no = str(bill_no or "")

        self.on_complete = on_complete
        self.on_payment_start = on_payment_start
        self.on_payment_cancel = on_payment_cancel

        # -----------------------------------------------------
        # Payment state
        # -----------------------------------------------------

        self.payment_mode = tk.StringVar(value="Cash")

        self.received = tk.StringVar(value=f"{self.total:.2f}")

        self.balance = tk.StringVar(value="₹ 0.00")

        self.status = tk.StringVar(value="Ready")

        self.status_detail = tk.StringVar(
            value="Enter the amount received from the customer."
        )

        # -----------------------------------------------------
        # UPI
        # -----------------------------------------------------

        self.upi_paid_var = tk.BooleanVar(value=False)
        self.upi_id = "8793432136-5@ybl"
        self.merchant_name = "QuickBill"

        self.upi_payload = ""
        self._upi_qr_photo = None

        self.upi_checkbox = None

        # -----------------------------------------------------
        # Card / Credit
        # -----------------------------------------------------

        self.card_paid_var = tk.BooleanVar(value=False)

        self.credit_confirm_var = tk.BooleanVar(value=False)

        # -----------------------------------------------------
        # Widget references
        # -----------------------------------------------------

        self.complete_button = None
        self.cancel_button = None
        self.received_entry = None
        self.balance_label = None

        self.status_indicator = None

        self.method_buttons = {}
        self.payment_area = None

        # -----------------------------------------------------
        # Lifecycle
        # -----------------------------------------------------

        self._processing = False
        self._closed = False
        self._parent_disabled = False

        self._received_trace = None
        self._display_notification_job = None

        # -----------------------------------------------------
        # Window
        # -----------------------------------------------------

        self._configure_window()
        self._configure_styles()
        self._build_ui()

        self._received_trace = self.received.trace_add(
            "write",
            self._on_received_changed,
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancel_payment,
        )

        self.bind(
            "<Escape>",
            self._on_escape,
        )

        self.bind(
            "<Return>",
            self._on_enter,
        )

        self._disable_parent_window()

        self.transient(parent)
        self.grab_set()

        self._center_on_parent()

        self.lift()
        self.focus_force()

        self.after(
            80,
            self._focus_initial_control,
        )

        self.after_idle(self.notify_payment_start)

    # =========================================================
    # WINDOW
    # =========================================================

    def _configure_window(self):

        self.title("QuickBill — Complete Payment")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        width = min(
            850,
            int(screen_width * 0.9),
        )

        height = min(
            750,
            int(screen_height * 0.9),
        )

        self.geometry(f"{width}x{height}")

        self.minsize(
            600,
            500,
        )

        self.resizable(
            True,
            True,
        )

        self.configure(bg=self.BG)

    def _configure_styles(self):
        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "QuickBill.TCheckbutton",
            background=self.CARD,
            foreground=self.TEXT,
            font=(
                "Segoe UI",
                10,
            ),
        )

    def _center_on_parent(self):

        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1:
            width = 760

        if height <= 1:
            height = 640

        screen_width = self.winfo_screenwidth()

        screen_height = self.winfo_screenheight()

        x = max(
            0,
            (screen_width - width) // 2,
        )

        y = max(
            0,
            (screen_height - height) // 2,
        )

        self.geometry(f"{width}x{height}+{x}+{y}")

    # =========================================================
    # MAIN WINDOW LOCK
    # =========================================================

    def _disable_parent_window(self):
        try:
            self.parent_window.attributes(
                "-disabled",
                True,
            )

            self._parent_disabled = True

        except (
            tk.TclError,
            AttributeError,
        ):
            self._parent_disabled = False

    def _restore_parent_window(self):
        if not self._parent_disabled:
            return

        try:
            self.parent_window.attributes(
                "-disabled",
                False,
            )
        except (
            tk.TclError,
            AttributeError,
        ):
            pass

        self._parent_disabled = False

        try:
            self.parent_window.deiconify()
            self.parent_window.lift()
            self.parent_window.focus_force()
        except Exception:
            pass

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):

        outer = tk.Frame(
            self,
            bg=self.BG,
            padx=18,
            pady=14,
        )

        outer.pack(
            fill="both",
            expand=True,
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            outer,
            bg=self.BG,
        )

        header.pack(
    fill="x",
    pady=(0, 5),
)

        tk.Label(
            header,
            text="QUICKBILL",
            bg=self.BG,
            fg=self.PRIMARY,
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Complete Payment",
            bg=self.BG,
            fg=self.TEXT,
            font=(
                "Segoe UI",
                19,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(1, 0),
        )

        tk.Label(
            header,
            text=(f"Invoice: {self.bill_no}" if self.bill_no else "Current Invoice"),
            bg=self.BG,
            fg=self.MUTED,
            font=(
                "Segoe UI",
                9,
            ),
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        # =====================================================
        # AMOUNT CARD
        # =====================================================

        amount_card = tk.Frame(
            outer,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        amount_card.pack(
    fill="x",
    pady=(0, 6),
)
        amount_content = tk.Frame(
            amount_card,
            bg=self.CARD,
        )

        amount_content.pack(
            fill="x",
            padx=16,
            pady=8,
        )

        left_amount = tk.Frame(
            amount_content,
            bg=self.CARD,
        )

        left_amount.pack(
            side="left",
            fill="x",
            expand=True,
        )

        tk.Label(
            left_amount,
            text="AMOUNT DUE",
            bg=self.CARD,
            fg=self.MUTED,
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
        ).pack(anchor="w")

        tk.Label(
            left_amount,
            text=f"₹ {self.total:,.2f}",
            bg=self.CARD,
            fg=self.SUCCESS,
            font=(
                "Segoe UI",
                25,
                "bold",
            ),
        ).pack(anchor="w")

        tk.Label(
            amount_content,
            text="PAYMENT",
            bg=self.SUCCESS_BG,
            fg=self.SUCCESS,
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
            padx=10,
            pady=5,
        ).pack(side="right")

        # =====================================================
        # PAYMENT METHOD CARD
        # =====================================================

        method_card = tk.Frame(
            outer,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        method_card.pack(
    fill="x",
    pady=(0, 6),
)

        tk.Label(
            method_card,
            text="PAYMENT METHOD",
            bg=self.CARD,
            fg=self.MUTED,
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
        ).pack(
            anchor="w",
            padx=13,
            pady=(8, 6),
        )

        self.method_buttons_frame = tk.Frame(
            method_card,
            bg=self.CARD,
        )

        self.method_buttons_frame.pack(
            fill="x",
            padx=9,
            pady=(0, 8),
        )

        for mode in self.PAYMENT_MODES:

            self._create_method_button(
                self.method_buttons_frame,
                mode,
            )

        # =====================================================
        # BOTTOM BUTTONS
        #
        # IMPORTANT:
        # These are packed BEFORE payment_area.
        # Therefore payment_area cannot hide them.
        # =====================================================

        button_frame = tk.Frame(
            outer,
            bg=self.BG,
            height=48,
        )

        button_frame.pack(
            fill="x",
            side="bottom",
            pady=(0, 0),
        )

        button_frame.pack_propagate(False)

        self.cancel_button = tk.Button(
            button_frame,
            text="Cancel Payment",
            command=self.cancel_payment,
            bg=self.CARD,
            fg=self.DANGER,
            activebackground=self.DANGER_BG,
            activeforeground=self.DANGER,
            disabledforeground="#a0a8b3",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            relief="flat",
            bd=0,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            cursor="hand2",
        )

        self.cancel_button.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5),
        )

        self.complete_button = tk.Button(
            button_frame,
            text="Complete Sale",
            command=self.complete_sale,
            bg="#94a3b8",
            fg="white",
            activebackground=self.SUCCESS_DARK,
            activeforeground="white",
            disabledforeground="#e5e7eb",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            relief="flat",
            bd=0,
            cursor="hand2",
        )

        self.complete_button.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 0),
        )

        # =====================================================
        # STATUS
        # =====================================================

        status_frame = tk.Frame(
            outer,
            bg=self.BG,
        )

        status_frame.pack(
            fill="x",
            side="bottom",
            pady=(0, 4),
        )

        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            bg=self.BG,
            fg=self.SUCCESS,
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
        )

        self.status_indicator.pack(side="left")

        tk.Label(
            status_frame,
            textvariable=self.status,
            bg=self.BG,
            fg=self.TEXT,
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
        ).pack(
            side="left",
            padx=(5, 4),
        )

        tk.Label(
            status_frame,
            textvariable=self.status_detail,
            bg=self.BG,
            fg=self.MUTED,
            font=(
                "Segoe UI",
                8,
            ),
        ).pack(
            side="left",
        )

        # =====================================================
        # DYNAMIC PAYMENT AREA
        #
        # This is intentionally packed LAST with expand=True.
        # It gets only the remaining space.
        # =====================================================

        self.payment_area = tk.Frame(
            outer,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        self.payment_area.pack(
            fill="both",
            expand=True,
            pady=(0, 5),
        )

        # DO NOT use pack_propagate(False) here.
        self.payment_area.pack_propagate(True)

        # =====================================================
        # INITIAL PAYMENT MODE
        # =====================================================

        self.payment_mode.set("Cash")

        self._build_cash_payment()

        # Make sure CASH is visibly selected.
        self._refresh_method_buttons()

        # Make Complete Sale available because received
        # amount initially equals total.
        self.update_complete_button()

        self.update_idletasks()

        self._center_on_parent()

        # =====================================================
        # INITIAL CUSTOMER DISPLAY SYNC
        # =====================================================

        self.after(
            100,
            self.notify_payment_start,
        )

    # =========================================================
    # PAYMENT METHOD BUTTONS
    # =========================================================

    def _create_method_button(
        self,
        parent,
        mode,
    ):

        button = tk.Button(
            parent,
            text=mode.upper(),
            command=lambda value=mode: self.set_payment_mode(value),
            bg=self.CARD,
            fg=self.TEXT,
            activebackground=self.BLUE_BG,
            activeforeground=self.PRIMARY,
            disabledforeground="#98a2b3",
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
            relief="flat",
            bd=0,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            cursor="hand2",
            height=2,
        )

        button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=3,
        )

        self.method_buttons[mode] = button

    def _refresh_method_buttons(self):

        current_mode = self.payment_mode.get()

        for mode, button in self.method_buttons.items():

            if mode == current_mode:

                button.configure(
                    bg=self.PRIMARY,
                    fg="white",
                    activebackground=self.PRIMARY_DARK,
                    activeforeground="white",
                    highlightbackground=self.PRIMARY,
                    highlightthickness=2,
                )

            else:

                button.configure(
                    bg=self.CARD,
                    fg=self.TEXT,
                    activebackground=self.BLUE_BG,
                    activeforeground=self.PRIMARY,
                    highlightbackground=self.BORDER,
                    highlightthickness=1,
                )

            # Only lock payment method switching while sale
            # is actually being processed.
            button.configure(state=("disabled" if self._processing else "normal"))

    # =========================================================
    # PAYMENT AREA
    # =========================================================

    def _clear_payment_area(self):

        if self.payment_area is None:
            return

        for widget in self.payment_area.winfo_children():
            widget.destroy()

        self.received_entry = None
        self.balance_label = None
        self._upi_qr_photo = None

    def set_payment_mode(self, mode):

        if self._processing or self._closed:
            return

        if mode not in self.PAYMENT_MODES:
            return

        self.payment_mode.set(mode)

        self.upi_paid_var.set(False)
        self.card_paid_var.set(False)
        self.credit_confirm_var.set(False)

        if mode != "UPI":
            self.upi_payload = ""

        self.payment_mode_changed()

        self.after(
            30,
            self.notify_payment_start,
        )

    def payment_mode_changed(self):

        if self._processing or self._closed:
            return

        mode = self.payment_mode.get()

        # Clear current payment content.
        self._clear_payment_area()

        # -----------------------------------------------------
        # Build selected payment screen
        # -----------------------------------------------------

        if mode == "Cash":

            self._build_cash_payment()

        elif mode == "UPI":

            self.build_upi_payment()

        elif mode == "Card":

            self.build_card_payment()

        elif mode == "Credit":

            self.build_credit_payment()

        # -----------------------------------------------------
        # Refresh selected tab
        # -----------------------------------------------------

        self._refresh_method_buttons()

        # -----------------------------------------------------
        # Refresh Complete Sale
        # -----------------------------------------------------

        self.update_complete_button()

        # -----------------------------------------------------
        # Cash gets focus
        # -----------------------------------------------------

        if mode == "Cash":

            self.after(
                50,
                self._focus_received_entry,
            )

    # =========================================================
    # CUSTOMER DISPLAY
    # =========================================================

    def _schedule_display_notification(self):

        if self._closed:
            return

        if self._display_notification_job is not None:

            try:
                self.after_cancel(self._display_notification_job)
            except tk.TclError:
                pass

        self._display_notification_job = self.after(
            30,
            self.notify_payment_start,
        )

    def _generate_qr_payload_only(self):

        from urllib.parse import quote

        amount = round(
            float(self.total),
            2,
        )

        params = [
            "pa="
            + quote(
                self.upi_id,
                safe="",
            ),
            "pn="
            + quote(
                self.merchant_name,
                safe="",
            ),
            f"am={amount:.2f}",
            "cu=INR",
        ]

        if self.bill_no:

            params.append(
                "tr="
                + quote(
                    self.bill_no,
                    safe="",
                )
            )

            params.append(
                "tn="
                + quote(
                    f"QuickBill-{self.bill_no}",
                    safe="",
                )
            )

        self.upi_payload = "upi://pay?" + "&".join(params)

        return self.upi_payload

    def notify_payment_start(self):

        if self._closed:
            return

        callback = self.on_payment_start

        if callback is None:
            print("[CustomerDisplay] " "No payment-start callback connected.")
            return

        mode = self.payment_mode.get()

        # -----------------------------------------------------
        # UPI
        # -----------------------------------------------------

        if mode == "UPI":

            try:

                payload = self._build_upi_payload()

                self.upi_payload = payload

                qr = {
                    "enabled": True,
                    "upi_id": self.upi_id,
                    "amount": float(self.total),
                    "payload": payload,
                    "merchant_name": self.merchant_name,
                }

            except Exception as exc:

                print("[CustomerDisplay] " f"UPI QR error: {exc}")

                qr = {
                    "enabled": False,
                    "upi_id": "",
                    "amount": float(self.total),
                    "payload": "",
                    "merchant_name": self.merchant_name,
                }

        # -----------------------------------------------------
        # CASH / CARD / CREDIT
        # -----------------------------------------------------

        else:

            qr = {
                "enabled": False,
                "upi_id": "",
                "amount": 0.0,
                "payload": "",
                "merchant_name": self.merchant_name,
            }

        # -----------------------------------------------------
        # Send state to Customer Display
        # -----------------------------------------------------

        try:

            callback(
                mode,
                float(self.total),
                qr,
            )

            print("[CustomerDisplay] " f"Payment state sent: {mode}")

        except TypeError:

            # Backward compatibility with your old callback.
            try:

                callback(
                    mode,
                    float(self.total),
                )

                print(
                    "[CustomerDisplay] "
                    f"Payment state sent using legacy callback: {mode}"
                )

            except Exception as exc:

                print("[CustomerDisplay] " f"Legacy callback failed: {exc}")

        except Exception as exc:

            print("[CustomerDisplay] " f"Payment state failed: {exc}")

    def _notify_payment_cancel(self):

        callback = self.on_payment_cancel

        if callback is None:
            return

        try:

            callback(self.payment_mode.get())

        except Exception as exc:

            print("[CustomerDisplay] " f"Payment cancellation failed: {exc}")

    # =========================================================
    # UPI QR
    # =========================================================

    def _build_upi_payload(self):

        if not self.upi_id:
            raise ValueError("Merchant UPI ID is missing.")

        amount = round(
            float(self.total),
            2,
        )

        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        params = [
            (
                "pa="
                + quote(
                    self.upi_id,
                    safe="",
                )
            ),
            (
                "pn="
                + quote(
                    self.merchant_name,
                    safe="",
                )
            ),
            (f"am={amount:.2f}"),
            "cu=INR",
        ]

        if self.bill_no:

            params.append(
                "tr="
                + quote(
                    self.bill_no,
                    safe="",
                )
            )

            params.append(
                "tn="
                + quote(
                    f"QuickBill-{self.bill_no}",
                    safe="",
                )
            )

        return "upi://pay?" + "&".join(params)

    def _generate_qr(self, parent):

        if not QR_AVAILABLE:
            raise RuntimeError("QR support requires " "qrcode and Pillow.")

        payload = self._build_upi_payload()

        qr = qrcode.QRCode(
            version=None,
            error_correction=(qrcode.constants.ERROR_CORRECT_M),
            box_size=8,
            border=4,
        )

        qr.add_data(payload)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        ).convert("RGB")

        image = image.resize((155, 155))

        self.upi_payload = payload

        self._upi_qr_photo = ImageTk.PhotoImage(
            image,
            master=parent,
        )

        return self._upi_qr_photo

    # =========================================================
    # CASH
    # =========================================================

    def _build_cash_payment(self):

        self.status.set("Ready")
        self.status_detail.set("Enter the amount received.")

        container = tk.Frame(
            self.payment_area,
            bg=self.CARD,
            padx=12,
            pady=8,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        tk.Label(
            container,
            text="CASH PAYMENT",
            bg=self.CARD,
            fg=self.SUCCESS,
            font=(
                "Segoe UI",
                13,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(0, 5),
        )

        # -----------------------------------------------------
        # Received amount
        # -----------------------------------------------------

        tk.Label(
            container,
            text="Received Amount",
            bg=self.CARD,
            fg=self.TEXT,
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(0, 3),
        )

        received_frame = tk.Frame(
            container,
            bg="#f8fafc",
            highlightbackground=self.BORDER,
            highlightthickness=1,
            height=50,
        )

        received_frame.pack(
            fill="x",
            pady=(0, 7),
        )

        received_frame.pack_propagate(False)

        self.received_entry = tk.Entry(
            received_frame,
            textvariable=self.received,
            justify="right",
            font=(
                "Segoe UI",
                19,
                "bold",
            ),
            bg="#f8fafc",
            fg=self.TEXT,
            relief="flat",
            bd=0,
            insertbackground=self.PRIMARY,
        )

        self.received_entry.pack(
            fill="both",
            expand=True,
            padx=8,
        )

        self.received_entry.bind(
            "<KeyRelease>",
            lambda event: self.calculate_balance(),
        )

        # -----------------------------------------------------
        # CHANGE TO RETURN
        # -----------------------------------------------------

        summary = tk.Frame(
            container,
            bg="#eff6ff",
            highlightbackground="#93c5fd",
            highlightthickness=1,
            height=62,
        )

        summary.pack(
            fill="x",
            pady=(0, 0),
        )

        summary.pack_propagate(False)

        summary_inner = tk.Frame(
            summary,
            bg="#eff6ff",
        )

        summary_inner.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5,
        )

        tk.Label(
            summary_inner,
            text="CHANGE TO RETURN",
            bg="#eff6ff",
            fg=self.PRIMARY,
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
        ).pack(
            anchor="w",
        )

        self.balance_label = tk.Label(
            summary_inner,
            textvariable=self.balance,
            bg="#eff6ff",
            fg=self.SUCCESS,
            font=(
                "Segoe UI",
                20,
                "bold",
            ),
        )

        self.balance_label.pack(
            anchor="w",
        )

        # -----------------------------------------------------
        # Initial calculation
        # -----------------------------------------------------

        self.calculate_balance()

        self.after(
            50,
            self.update_complete_button,
        )

    def set_received(self, amount):

        if self._processing:
            return

        try:
            value = float(amount)
        except (
            TypeError,
            ValueError,
        ):
            return

        self.received.set(f"{value:.2f}")

        self._focus_received_entry()

    # =========================================================
    # UPI
    # =========================================================

    def build_upi_payment(self):

        self.status.set("Awaiting UPI payment")

        self.status_detail.set("Scan the QR code and confirm the payment.")

        container = tk.Frame(
            self.payment_area,
            bg=self.CARD,
            padx=12,
            pady=8,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        # =====================================================
        # LEFT SIDE
        # =====================================================

        left = tk.Frame(
            container,
            bg=self.CARD,
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(4, 10),
        )

        tk.Label(
            left,
            text="UPI PAYMENT",
            bg=self.CARD,
            fg=self.PRIMARY,
            font=(
                "Segoe UI",
                13,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(0, 5),
        )

        # -----------------------------------------------------
        # Amount
        # -----------------------------------------------------

        amount_box = tk.Frame(
            left,
            bg=self.BLUE_BG,
            highlightbackground="#bfdbfe",
            highlightthickness=1,
        )

        amount_box.pack(
            fill="x",
            pady=(0, 7),
        )

        tk.Label(
            amount_box,
            text="AMOUNT TO PAY",
            bg=self.BLUE_BG,
            fg=self.PRIMARY,
            font=(
                "Segoe UI",
                7,
                "bold",
            ),
        ).pack(
            anchor="w",
            padx=10,
            pady=(5, 0),
        )

        tk.Label(
            amount_box,
            text=f"₹ {self.total:,.2f}",
            bg=self.BLUE_BG,
            fg=self.PRIMARY,
            font=(
                "Segoe UI",
                20,
                "bold",
            ),
        ).pack(
            anchor="w",
            padx=10,
            pady=(0, 5),
        )

        # -----------------------------------------------------
        # Merchant UPI ID
        # -----------------------------------------------------

        upi_box = tk.Frame(
            left,
            bg="#f8fafc",
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        upi_box.pack(
            fill="x",
            pady=(0, 7),
        )

        tk.Label(
            upi_box,
            text="MERCHANT UPI ID",
            bg="#f8fafc",
            fg=self.MUTED,
            font=(
                "Segoe UI",
                7,
                "bold",
            ),
        ).pack(
            anchor="w",
            padx=10,
            pady=(5, 0),
        )

        tk.Label(
            upi_box,
            text=self.upi_id,
            bg="#f8fafc",
            fg=self.PRIMARY,
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
        ).pack(
            anchor="w",
            padx=10,
            pady=(0, 5),
        )

   

        # -----------------------------------------------------
        # UPI PAYMENT CONFIRMATION
        # -----------------------------------------------------

        confirm_frame = tk.Frame(
            left,
            bg=self.CARD,
        )

        confirm_frame.pack(
            fill="x",
            pady=(5, 0),
        )

        self.upi_checkbox = tk.Checkbutton(
            confirm_frame,
            text="I have received the UPI payment",
            variable=self.upi_paid_var,
            command=self.update_complete_button,

            bg=self.CARD,
            fg=self.TEXT,

            activebackground=self.CARD,
            activeforeground=self.TEXT,

            selectcolor="#dbeafe",

            font=(
                "Segoe UI",
                9,
                "bold",
            ),

            relief="flat",
            bd=0,

            cursor="hand2",

            anchor="w",

            padx=2,
            pady=2,
        )

        self.upi_checkbox.pack(
            anchor="w",
        )

        tk.Label(
            confirm_frame,
            text="Confirm after verifying the payment.",
            bg=self.CARD,
            fg=self.MUTED,
            font=(
                "Segoe UI",
                7,
            ),
        ).pack(
            anchor="w",
            padx=(25, 0),
        )

        # =====================================================
        # RIGHT SIDE — QR
        # =====================================================

        right = tk.Frame(
            container,
            bg="#f8fafc",
            width=210,
            height=198,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        right.pack(
            side="right",
            fill="y",
        )

        right.pack_propagate(False)

        tk.Label(
            right,
            text="SCAN TO PAY",
            bg="#f8fafc",
            fg=self.PRIMARY,
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
        ).pack(
            pady=(5, 3),
        )

        qr_frame = tk.Frame(
            right,
            bg="white",
            width=165,
            height=165,
            highlightbackground=self.BORDER,
            highlightthickness=1,
        )

        qr_frame.pack(
            pady=(0, 3),
        )

        qr_frame.pack_propagate(False)

        try:

            qr_photo = self._generate_qr(qr_frame)

            tk.Label(
                qr_frame,
                image=qr_photo,
                bg="white",
                bd=0,
            ).pack(
                expand=True,
            )

        except Exception as exc:

            tk.Label(
                qr_frame,
                text="Unable to generate QR",
                bg="white",
                fg=self.DANGER,
                font=(
                    "Segoe UI",
                    8,
                    "bold",
                ),
            ).pack(
                expand=True,
            )

            print(
                "[UPI] QR generation failed:",
                exc,
            )

        tk.Label(
            right,
            text="Amount included in QR",
            bg="#f8fafc",
            fg=self.MUTED,
            font=(
                "Segoe UI",
                7,
            ),
        ).pack()

        tk.Label(
            right,
            text=f"₹ {self.total:,.2f}",
            bg="#f8fafc",
            fg=self.SUCCESS,
            font=(
                "Segoe UI",
                11,
                "bold",
            ),
        ).pack(
            pady=(0, 2),
        )

    # =========================================================
    # CARD
    # =========================================================

    def build_card_payment(self):

        self.status.set("Awaiting card payment")

        self.status_detail.set("Process the amount using the card terminal.")

        container = tk.Frame(
            self.payment_area,
            bg=self.CARD,
            padx=18,
            pady=16,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        tk.Label(
            container,
            text="CARD PAYMENT",
            bg=self.CARD,
            fg="#6d28d9",
            font=(
                "Segoe UI",
                13,
                "bold",
            ),
        ).pack(anchor="w")

        tk.Label(
            container,
            text=f"₹ {self.total:,.2f}",
            bg="#f5f3ff",
            fg="#5b21b6",
            font=(
                "Segoe UI",
                23,
                "bold",
            ),
            pady=12,
        ).pack(
            fill="x",
            pady=(8, 14),
        )

        tk.Label(
            container,
            text=("Process the payment using the " "connected card terminal."),
            bg=self.CARD,
            fg=self.MUTED,
            font=(
                "Segoe UI",
                9,
            ),
        ).pack(anchor="w")

        ttk.Checkbutton(
            container,
            text="Card payment has been received",
            variable=self.card_paid_var,
            command=self.update_complete_button,
            style="QuickBill.TCheckbutton",
        ).pack(
            anchor="w",
            pady=(14, 2),
        )

    # =========================================================
    # CREDIT
    # =========================================================

    def build_credit_payment(self):

        self.status.set("Credit sale confirmation")

        self.status_detail.set("Confirm that this sale should be recorded as credit.")

        container = tk.Frame(
            self.payment_area,
            bg=self.CARD,
            padx=18,
            pady=16,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        tk.Label(
            container,
            text="CREDIT SALE",
            bg=self.CARD,
            fg=self.WARNING,
            font=(
                "Segoe UI",
                13,
                "bold",
            ),
        ).pack(anchor="w")

        tk.Label(
            container,
            text=f"₹ {self.total:,.2f}",
            bg=self.WARNING_BG,
            fg="#92400e",
            font=(
                "Segoe UI",
                23,
                "bold",
            ),
            pady=12,
        ).pack(
            fill="x",
            pady=(8, 14),
        )

        tk.Label(
            container,
            text=("Confirm that this sale should " "be recorded as credit."),
            bg=self.CARD,
            fg=self.MUTED,
            font=(
                "Segoe UI",
                9,
            ),
        ).pack(anchor="w")

        ttk.Checkbutton(
            container,
            text="Confirm credit sale",
            variable=self.credit_confirm_var,
            command=self.update_complete_button,
            style="QuickBill.TCheckbutton",
        ).pack(
            anchor="w",
            pady=(14, 2),
        )

    # =========================================================
    # CASH VALIDATION
    # =========================================================

    def _on_received_changed(
        self,
        *_,
    ):

        if self.payment_mode.get() == "Cash":
            self.calculate_balance()

    def calculate_balance(self):

        if self.payment_mode.get() != "Cash":
            return

        try:
            received = float(str(self.received.get()).strip())

        except (
            TypeError,
            ValueError,
        ):
            received = 0.0

        change = received - self.total

        self.balance.set(f"₹ {change:,.2f}")

        if self.balance_label is None:
            self.update_complete_button()
            return

        if received >= self.total:

            self.balance_label.configure(
                fg=self.SUCCESS,
                bg="#eff6ff",
            )

            self.status.set("Ready")

            self.status_detail.set(f"Change to return: ₹ {change:,.2f}")

            if hasattr(self, "status_indicator"):
                self.status_indicator.configure(fg=self.SUCCESS)

        else:

            short = self.total - received

            self.balance_label.configure(
                fg=self.DANGER,
                bg="#eff6ff",
            )

            self.status.set("Insufficient amount")

            self.status_detail.set(f"₹ {short:,.2f} more required.")

            if hasattr(self, "status_indicator"):
                self.status_indicator.configure(fg=self.DANGER)

        self.update_complete_button()

    # =========================================================
    # STATUS
    # =========================================================

    def _set_status_indicator(
        self,
        color,
    ):

        if self.status_indicator is not None:

            try:
                self.status_indicator.configure(fg=color)
            except tk.TclError:
                pass

    # =========================================================
    # BUTTON STATE
    # =========================================================

    def _cash_is_valid(self):

        try:

            received_str = str(self.received.get()).strip()
            if not received_str:
                return False

            received = float(received_str)

        except (
            TypeError,
            ValueError,
        ):

            return False

        return received >= self.total

    def update_complete_button(self):

        if self.complete_button is None:
            return

        if self._processing:

            self.complete_button.configure(
                state="disabled",
                text="Processing...",
                bg=BG_DISABLED,
                fg=TEXT_DISABLED,
                cursor="",
            )

            if self.cancel_button is not None:
                self.cancel_button.configure(state="disabled")

            self._refresh_method_buttons()

            return

        mode = self.payment_mode.get()

        if mode == "Cash":

            enabled = self._cash_is_valid()

        elif mode == "UPI":

            enabled = bool(self.upi_paid_var.get())

        elif mode == "Card":

            enabled = bool(self.card_paid_var.get())

        elif mode == "Credit":

            enabled = bool(self.credit_confirm_var.get())

        else:

            enabled = False

        self.complete_button.configure(
            state=("normal" if enabled else "disabled"),
            text="Complete Sale",
            bg=(self.SUCCESS if enabled else BG_DISABLED),
            fg=(self.CARD if enabled else TEXT_DISABLED),
            cursor=("hand2" if enabled else ""),
        )

        if self.cancel_button is not None:

            self.cancel_button.configure(state="normal")

        self._refresh_method_buttons()

    # =========================================================
    # FOCUS / KEYBOARD
    # =========================================================

    def _focus_initial_control(self):

        if self._closed:
            return

        if self.payment_mode.get() == "Cash":

            self._focus_received_entry()

        else:

            try:
                self.focus_force()
            except tk.TclError:
                pass

    def _focus_received_entry(self):

        if (
            self.received_entry is None
            or self.payment_mode.get() != "Cash"
            or self._processing
        ):
            return

        try:

            self.received_entry.focus_set()

            self.received_entry.select_range(
                0,
                tk.END,
            )

        except tk.TclError:
            pass

    def _on_escape(
        self,
        _event=None,
    ):

        self.cancel_payment()

    def _on_enter(
        self,
        _event=None,
    ):

        if not self._processing:

            self.complete_sale()

    # =========================================================
    # COMPLETE SALE
    # =========================================================

    def complete_sale(self):

        if self._processing or self._closed:
            return

        mode = self.payment_mode.get()

        # -----------------------------------------------------
        # Cash
        # -----------------------------------------------------

        if mode == "Cash":

            try:

                received = float(str(self.received.get()).strip())

            except (
                TypeError,
                ValueError,
            ):

                show_error(
                    self,
                    "Invalid Amount",
                    "Please enter a valid received amount.",
                )

                self._focus_received_entry()

                return

            if received < self.total:

                show_warning(
                    self,
                    "Insufficient Amount",
                    (
                        f"Received amount: "
                        f"₹ {received:,.2f}\n\n"
                        f"Required amount: "
                        f"₹ {self.total:,.2f}"
                    ),
                )

                self._focus_received_entry()

                return

        # -----------------------------------------------------
        # UPI
        # -----------------------------------------------------

        elif mode == "UPI":

            if not self.upi_paid_var.get():

                return

            received = self.total

        # -----------------------------------------------------
        # Card
        # -----------------------------------------------------

        elif mode == "Card":

            if not self.card_paid_var.get():

                return

            received = self.total

        # -----------------------------------------------------
        # Credit
        # -----------------------------------------------------

        elif mode == "Credit":

            if not self.credit_confirm_var.get():

                return

            received = self.total

        else:

            return

        # -----------------------------------------------------
        # Lock immediately
        # -----------------------------------------------------

        self._processing = True

        self.status.set("Processing")

        self.status_detail.set("Completing the sale. Please wait...")

        self._set_status_indicator(self.PRIMARY)

        self.update_complete_button()

        self.update_idletasks()

        # -----------------------------------------------------
        # Desktop completion callback
        # -----------------------------------------------------

        try:

            result = self.on_complete(
                mode,
                received,
            )

            # False means the desktop transaction failed.
            if result is False:

                self._processing = False

                self.status.set("Unable to complete")

                self.status_detail.set("Correct the issue and try again.")

                self._set_status_indicator(self.DANGER)

                self.update_complete_button()

                return

        except Exception as exc:

            self._processing = False

            self.status.set("Payment error")

            self.status_detail.set("The sale could not be completed.")

            self._set_status_indicator(self.DANGER)

            self.update_complete_button()

            show_error(
                self,
                "Payment Error",
                ("Unable to complete the sale.\n\n" f"{exc}"),
            )

            return

        # -----------------------------------------------------
        # Success
        # -----------------------------------------------------

        self._close_after_success()

    # =========================================================
    # SUCCESS CLOSE
    # =========================================================

    def _close_after_success(self):

        if self._closed:
            return

        self._closed = True

        self._cancel_display_job()

        self._restore_parent_window()

        try:
            self.grab_release()
        except tk.TclError:
            pass

        try:
            self.destroy()
        except tk.TclError:
            pass

    # =========================================================
    # CANCEL
    # =========================================================

    def cancel_payment(self):

        if self._processing or self._closed:
            return

        confirmed = show_confirmation(
            self,
            "Cancel Payment",
            ("Are you sure you want to cancel " "this payment?"),
        )

        if not confirmed:
            return

        self._closed = True

        self._cancel_display_job()

        # Notify Android BEFORE destroying the dialog.
        self._notify_payment_cancel()

        self._restore_parent_window()

        try:
            self.grab_release()
        except tk.TclError:
            pass

        try:
            self.destroy()
        except tk.TclError:
            pass

    # =========================================================
    # CLEANUP
    # =========================================================

    def _cancel_display_job(self):

        if self._display_notification_job is None:
            return

        try:

            self.after_cancel(self._display_notification_job)

        except tk.TclError:
            pass

        self._display_notification_job = None
