import tkinter as tk


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

        tk.Label(row1, text="Barcode", bg="white", font=("Segoe UI", 10, "bold")).pack(
            side="left"
        )

        self.barcode_entry = tk.Entry(row1, width=30, font=("Consolas", 14))

        self.barcode_entry.pack(side="left", padx=10)

        self.add_button = tk.Button(
            row1, text="Add", width=10, bg="#1f7ae0", fg="white"
        )

        self.add_button.pack(side="left")

        # ---------- Scan Controls ----------

        control_row = tk.Frame(self, bg="white")
        control_row.pack(fill="x", padx=10, pady=(0, 5))

        self.scan_button = tk.Button(
            control_row,
            text="▶ Start Scan",
            width=16,
            bg="#007bff",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.toggle_scan,
        )

        self.scan_button.pack(side="left")

        # ---------- Product Details ----------

        row2 = tk.Frame(self, bg="white")
        row2.pack(fill="x", padx=10, pady=8)

        self.product = tk.StringVar(value="-")
        self.barcode = tk.StringVar(value="-")
        self.brand = tk.StringVar(value="-")
        self.category = tk.StringVar(value="-")
        self.price = tk.StringVar(value="₹0.00")
        self.gst = tk.StringVar(value="0 %")
        self.stock = tk.StringVar(value="0")
        self.status = tk.StringVar(value="Ready")

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
            box.pack(side="left", expand=True)

            tk.Label(
                box, text=title, bg="white", fg="gray", font=("Segoe UI", 9)
            ).pack()

            tk.Label(
                box,
                textvariable=var,
                bg="white",
                fg="#1d3557",
                font=("Segoe UI", 11, "bold"),
            ).pack()

    def get_barcode(self):
        return self.barcode_entry.get().strip()

    def clear(self):
        self.barcode_entry.delete(0, tk.END)

    def focus(self):
        self.barcode_entry.focus()

    def set_scan_callbacks(self, start_callback=None, stop_callback=None):
        self._start_scan_callback = start_callback
        self._stop_scan_callback = stop_callback

    def start_scan(self):
        if self._start_scan_callback:
            self._start_scan_callback()

    def stop_scan(self):
        if self._stop_scan_callback:
            self._stop_scan_callback()

    def update_status(self, text):
        self.status.set(text)

    def display_product(self, product):

        self.barcode.set(product.get("barcode", "-"))

        self.product.set(product.get("name", "-"))

        self.brand.set(product.get("brand", "-"))

        self.category.set(product.get("category", "-"))

        self.price.set(f"₹ {product.get('selling_price', 0):.2f}")

        self.gst.set(f"{product.get('gst',0)} %")

        self.stock.set(str(product.get("stock", 0)))

        self.status.set("Ready")

    def toggle_scan(self):

        if self.scan_button["text"] == "▶ Start Scan":

            self.start_scan()

            self.scan_button.config(
                text="■ Stop Scan",
                bg="#dc3545",
            )

        else:

            self.stop_scan()

            self.scan_button.config(
                text="▶ Start Scan",
                bg="#007bff",
            )

    def set_status(self, text):
        self.update_status(text)
