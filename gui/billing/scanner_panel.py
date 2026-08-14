import tkinter as tk
from gui.ui_components import create_primary_button, create_danger_button, FONT_INPUT, PRIMARY, DANGER
from logic.config import get_currency


class ScannerPanel(tk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent, text="Product Scanner", bg="white", font=("Segoe UI", 10, "bold")
        )

        self._start_scan_callback = None
        self._stop_scan_callback = None

        # ---------- Barcode ----------

        row1 = tk.Frame(self, bg="white")
        row1.pack(fill="x", padx=10, pady=5)

        tk.Label(
            row1,
            text="Barcode :",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left")

        self.barcode_entry = tk.Entry(
            row1,
            font=("Consolas", 12),
            width=45,
            fg="gray"
        )
        self.barcode_entry.insert(0, "Scan or type barcode")
        
        def on_focus_in(event):
            if self.barcode_entry.get() == "Scan or type barcode":
                self.barcode_entry.delete(0, tk.END)
                self.barcode_entry.config(fg="black")
                
        def on_focus_out(event):
            if not self.barcode_entry.get():
                self.barcode_entry.insert(0, "Scan or type barcode")
                self.barcode_entry.config(fg="gray")

        self.barcode_entry.bind("<FocusIn>", on_focus_in)
        self.barcode_entry.bind("<FocusOut>", on_focus_out)
        self.barcode_entry.bind("<Return>", lambda e: self.add_button.invoke())

        self.barcode_entry.pack(side="left", padx=(8, 3))

        self.add_button = create_primary_button(
            row1,
            "Add",
            width=10,
            height=1
        )

        self.add_button.pack(side="left")

        # ---------- Scan Controls ----------

        control_row = tk.Frame(self, bg="white")
        control_row.pack(fill="x", padx=10, pady=(0, 5))

        self.scan_button = create_primary_button(
            control_row,
            "▶ Start Scan",
            command=self.toggle_scan,
            width=16,
        )

        self.scan_button.pack(anchor="w", pady=(2, 0))

        # ---------- Product Details ----------

        row2 = tk.Frame(self, bg="white")
        row2.pack(fill="x", padx=10, pady=2)

        self.product = tk.StringVar(value="-")
        self.barcode = tk.StringVar(value="-")
        self.brand = tk.StringVar(value="-")
        self.category = tk.StringVar(value="-")
        self.price = tk.StringVar(value="-")
        self.gst = tk.StringVar(value="-")
        self.stock = tk.StringVar(value="-")
        self.status = tk.StringVar(value="-")

        data = [
            ("Barcode", self.barcode),
            ("Product", self.product),
            ("Brand", self.brand),
            ("Category", self.category),
            ("Price", self.price),
            ("GST", self.gst),
            ("Stock", self.stock),
            ("Status", self.status),
        ]

        for title, var in data:

            box = tk.Frame(row2, bg="white")
            box.pack(side="left", padx=15)

            tk.Label(
                box, text=title, bg="white", fg="gray", font=("Segoe UI", 9)
            ).pack()

            tk.Label(
                box,
                textvariable=var,
                bg="white",
                fg="#1d3557",
                font=("Segoe UI", 10, "bold"),
            ).pack(pady=(0, 2))

    def get_barcode(self):
        val = self.barcode_entry.get().strip()
        return "" if val == "Scan or type barcode" else val

    def clear(self):
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.insert(0, "Scan or type barcode")
        self.barcode_entry.config(fg="gray")

    def focus(self):
        self.barcode_entry.focus()

    def set_scan_callbacks(self, start_callback=None, stop_callback=None):
        self._start_scan_callback = start_callback
        self._stop_scan_callback = stop_callback

    def update_status(self, text):
        self.status.set(text)

    def display_product(self, product):

        self.barcode.set(product.get("barcode", "-"))

        self.product.set(product.get("name", "-"))

        self.brand.set(product.get("brand", "-"))

        self.category.set(product.get("category", "-"))

        self.price.set(f"{get_currency()} {product.get('selling_price', 0):.2f}")

        self.gst.set(f"{product.get('gst',0)} %")

        self.stock.set(str(product.get("stock", 0)))

        self.status.set("-")

    def toggle_scan(self):

        if self.scan_button["text"] == "▶ Start Scan":

            self.scan_button.config(
                text="■ Stop Scan",
                bg=DANGER,
            )
            self.scan_button._qb_style["bg"] = DANGER

            if self._start_scan_callback:
                self._start_scan_callback()

        else:

            self.scan_button.config(
                text="▶ Start Scan",
                bg=PRIMARY,
            )
            self.scan_button._qb_style["bg"] = PRIMARY

            if self._stop_scan_callback:
                self._stop_scan_callback()

    def set_status(self, text):
        self.update_status(text)
