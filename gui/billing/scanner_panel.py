import tkinter as tk
from gui.ui_components import create_primary_button, create_danger_button, FONT_INPUT, PRIMARY, DANGER
from logic.config import get_currency
from logic.database import get_all_products


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

        self.barcode_var = tk.StringVar()
        self.barcode_entry = tk.Entry(
            row1,
            textvariable=self.barcode_var,
            font=("Consolas", 12),
            width=45,
        )
        self.barcode_entry.pack(side="left", padx=(8, 3))
        
        # --- Floating Listbox Setup ---
        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)
        self.popup.withdraw()
        
        self.listbox = tk.Listbox(self.popup, font=("Segoe UI", 11), bg="white", fg="black", selectbackground="#0d6efd", selectforeground="white")
        self.listbox.pack(fill="both", expand=True)
        
        self._all_products = get_all_products()
        
        # --- Bindings ---
        self.barcode_entry.bind("<KeyRelease>", self._on_keyrelease)
        self.barcode_entry.bind("<Down>", self._on_down)
        self.barcode_entry.bind("<Up>", self._on_up)
        self.barcode_entry.bind("<Return>", self._on_return)
        self.barcode_entry.bind("<FocusOut>", lambda e: self.after(150, self.popup.withdraw))
        self.listbox.bind("<ButtonRelease-1>", self._on_listbox_click)

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
        if " - " in val:
            val = val.split(" - ")[0].strip()
        return val

    def clear(self):
        self.barcode_entry.delete(0, tk.END)
        self.barcode_entry.focus()

    def focus(self):
        self.barcode_entry.focus()

    def _on_keyrelease(self, event):
        if event.keysym in ("Up", "Down", "Return", "Tab"):
            return
            
        typed = self.barcode_var.get().lower()
        if not typed:
            matches = [f"{p.get('barcode', '')} - {p.get('name', '')}" for p in self._all_products]
        else:
            matches = []
            for p in self._all_products:
                b = p.get("barcode", "")
                n = p.get("name", "")
                if typed in b.lower() or typed in n.lower():
                    matches.append(f"{b} - {n}")
                    
        self.listbox.delete(0, tk.END)
        for m in matches:
            self.listbox.insert(tk.END, m)
            
        if matches:
            # Adjust popup height based on items (max 8)
            h = min(len(matches) * 22, 176)
            self.popup.geometry(f"{self.barcode_entry.winfo_width()}x{h}+{self.barcode_entry.winfo_rootx()}+{self.barcode_entry.winfo_rooty() + self.barcode_entry.winfo_height()}")
            self.popup.deiconify()
            self.popup.lift()
        else:
            self.popup.withdraw()
            
    def _on_down(self, event):
        if self.popup.winfo_ismapped():
            sel = self.listbox.curselection()
            if not sel:
                self.listbox.selection_set(0)
            else:
                idx = sel[0]
                if idx < self.listbox.size() - 1:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(idx + 1)
            self.listbox.see(self.listbox.curselection()[0])
            return "break"
            
    def _on_up(self, event):
        if self.popup.winfo_ismapped():
            sel = self.listbox.curselection()
            if sel:
                idx = sel[0]
                if idx > 0:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(idx - 1)
                self.listbox.see(self.listbox.curselection()[0])
            return "break"
            
    def _on_return(self, event):
        if self.popup.winfo_ismapped():
            sel = self.listbox.curselection()
            if sel:
                val = self.listbox.get(sel[0])
                self.barcode_entry.delete(0, tk.END)
                self.barcode_entry.insert(0, val)
                self.popup.withdraw()
                self.add_button.invoke()
                return "break"
        self.add_button.invoke()
        
    def _on_listbox_click(self, event):
        sel = self.listbox.curselection()
        if sel:
            val = self.listbox.get(sel[0])
            self.barcode_entry.delete(0, tk.END)
            self.barcode_entry.insert(0, val)
            self.popup.withdraw()
            self.barcode_entry.focus_set()
            self.add_button.invoke()


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
