import tkinter as tk
import datetime


class Header(tk.Frame):

    COLORS = {
        "bg": "#16324F",
        "text": "#FFFFFF",
        "muted": "#B8C7D6",
        "subtle": "#8FA4B8",
        "border": "#2A4967",
        "accent": "#2F6FED",
    }

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=self.COLORS["bg"],
            height=82,
            bd=0,
            highlightthickness=0,
        )

        self.pack_propagate(False)

        self._build_ui()
        self.update_clock()

    # ============================================================
    # BUILD HEADER
    # ============================================================

    def _build_ui(self):

        bg = self.COLORS["bg"]

        content = tk.Frame(
            self,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )

        content.pack(
            fill="both",
            expand=True,
            padx=18,
        )

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=0)
        content.grid_rowconfigure(0, weight=1)

        # ========================================================
        # LEFT — BRANDING
        # ========================================================

        left = tk.Frame(
            content,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        left.grid_rowconfigure(0, weight=1)

        brand = tk.Frame(
            left,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )

        brand.grid(
            row=0,
            column=0,
            sticky="w",
        )

        # Small brand accent
        accent = tk.Frame(
            brand,
            bg=self.COLORS["accent"],
            width=5,
            height=42,
        )

        accent.pack(
            side="left",
            padx=(0, 12),
        )

        accent.pack_propagate(False)

        brand_text = tk.Frame(
            brand,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )

        brand_text.pack(
            side="left",
        )

        self.title_label = tk.Label(
            brand_text,
            text="QuickBill Pro",
            font=("Segoe UI", 20, "bold"),
            fg=self.COLORS["text"],
            bg=bg,
            anchor="w",
            bd=0,
            padx=0,
            pady=0,
        )

        self.title_label.pack(
            anchor="w",
        )

        self.subtitle_label = tk.Label(
            brand_text,
            text="Professional Billing & POS",
            font=("Segoe UI", 8),
            fg=self.COLORS["muted"],
            bg=bg,
            anchor="w",
            bd=0,
            padx=0,
            pady=0,
        )

        self.subtitle_label.pack(
            anchor="w",
            pady=(1, 0),
        )

        # ========================================================
        # RIGHT — OPERATOR + CLOCK
        # ========================================================

        right = tk.Frame(
            content,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )

        right.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        right.grid_rowconfigure(0, weight=1)

        # --------------------------------------------------------
        # OPERATOR
        # --------------------------------------------------------

        operator = tk.Frame(
            right,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )

        operator.grid(
            row=0,
            column=0,
            sticky="e",
            padx=(0, 22),
        )

        self.operator_caption = tk.Label(
            operator,
            text="OPERATOR",
            font=("Segoe UI", 7, "bold"),
            fg=self.COLORS["subtle"],
            bg=bg,
            anchor="e",
        )

        self.operator_caption.pack(
            anchor="e",
        )

        self.operator_label = tk.Label(
            operator,
            text="Admin",
            font=("Segoe UI", 9, "bold"),
            fg=self.COLORS["text"],
            bg=bg,
            anchor="e",
        )

        self.operator_label.pack(
            anchor="e",
            pady=(2, 0),
        )

        # --------------------------------------------------------
        # SEPARATOR
        # --------------------------------------------------------

        separator = tk.Frame(
            right,
            bg=self.COLORS["border"],
            width=1,
        )

        separator.grid(
            row=0,
            column=1,
            sticky="ns",
            pady=16,
        )

        separator.grid_propagate(False)

        # --------------------------------------------------------
        # DATE / TIME
        # --------------------------------------------------------

        system = tk.Frame(
            right,
            bg=bg,
            bd=0,
            highlightthickness=0,
        )

        system.grid(
            row=0,
            column=2,
            sticky="e",
            padx=(20, 0),
        )

        self.time_label = tk.Label(
            system,
            text="",
            font=("Segoe UI", 12, "bold"),
            fg=self.COLORS["text"],
            bg=bg,
            anchor="e",
        )

        self.time_label.pack(
            anchor="e",
        )

        self.date_label = tk.Label(
            system,
            text="",
            font=("Segoe UI", 8),
            fg=self.COLORS["muted"],
            bg=bg,
            anchor="e",
        )

        self.date_label.pack(
            anchor="e",
            pady=(2, 0),
        )

    # ============================================================
    # LIVE CLOCK
    # ============================================================

    def update_clock(self):

        now = datetime.datetime.now()

        self.time_label.config(
            text=now.strftime("%I:%M:%S %p")
        )

        self.date_label.config(
            text=now.strftime("%A, %d %B %Y")
        )

        self._clock_job = self.after(
            1000,
            self.update_clock,
        )

    # ============================================================
    # OPERATOR
    # ============================================================

    def set_operator(self, name):

        if not name:
            name = "Admin"

        self.operator_label.config(
            text=str(name),
        )

    # ============================================================
    # CLEANUP
    # ============================================================

    def destroy(self):

        try:
            self.after_cancel(self._clock_job)
        except (AttributeError, tk.TclError):
            pass

        super().destroy()