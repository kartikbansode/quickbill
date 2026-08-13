import tkinter as tk
from tkinter import ttk, messagebox

from gui.dialogs.barcode_print_dialog import BarcodePrintDialog
from gui.dialogs.add_product_dialog import AddProductDialog
from logic.database import (
    get_all_products,
    search_products,
    get_product_by_barcode,
    delete_product,
)


class ProductMaster(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent, bg="#e9ecef")

        self.create_widgets()
        self.refresh_table()

    # =====================================================
    # UI
    # =====================================================

    def create_widgets(self):

        title = tk.Label(
            self,
            text="Products",
            font=("Segoe UI", 20, "bold"),
            bg="#e9ecef",
            fg="#1f2937",
        )

        title.pack(anchor="w", padx=20, pady=(15, 10))

        self.product_frame = tk.LabelFrame(
            self,
            text="Product Management",
            bg="white",
            font=("Segoe UI", 11, "bold"),
        )

        self.product_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=(0, 10),
        )

        # Let the table area take all remaining available height.
        self.product_frame.grid_columnconfigure(0, weight=1)
        self.product_frame.grid_rowconfigure(1, weight=1)

        self.create_toolbar()
        self.create_table()

    # =====================================================
    # Toolbar
    # =====================================================

    def create_toolbar(self):

        self.toolbar_frame = tk.Frame(
            self.product_frame,
            bg="white",
        )

        self.toolbar_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=5,
        )

        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "height": 2,
            "relief": "flat",
            "bd": 0,
            "cursor": "hand2",
            "activeforeground": "white",
        }

        buttons = [
            {
                "text": "Add Product",
                "bg": "#16a34a",
                "hover": "#15803d",
                "width": 16,
                "command": self.add_product,
            },
            {
                "text": "Edit",
                "bg": "#f59e0b",
                "hover": "#d97706",
                "width": 12,
                "command": self.edit_product,
            },
            {
                "text": "Delete",
                "bg": "#dc2626",
                "hover": "#b91c1c",
                "width": 12,
                "command": self.delete_product,
            },
            {
                "text": "Print Barcodes",
                "bg": "#2563eb",
                "hover": "#1d4ed8",
                "width": 18,
                "command": self.print_barcodes,
            },
        ]

        for item in buttons:

            btn = tk.Button(
                self.toolbar_frame,
                text=item["text"],
                bg=item["bg"],
                fg="white",
                width=item["width"],
                command=item["command"],
                **button_style,
            )

            btn.pack(side=tk.LEFT, padx=(0, 8))

            btn.bind(
                "<Enter>",
                lambda e, b=btn, c=item["hover"]: b.config(bg=c),
            )

            btn.bind(
                "<Leave>",
                lambda e, b=btn, c=item["bg"]: b.config(bg=c),
            )

        # Spacer
        tk.Frame(
            self.toolbar_frame,
            bg="white",
        ).pack(side=tk.LEFT, expand=True, fill=tk.X)

        tk.Label(
            self.toolbar_frame,
            text="Search :",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            self.toolbar_frame,
            textvariable=self.search_var,
            width=30,
            font=("Segoe UI", 10),
        )

        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.focus_set()

        self.total_label = tk.StringVar(value="Products : 0")

        tk.Label(
            self.toolbar_frame,
            textvariable=self.total_label,
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.LEFT)

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_table(),
        )

    def print_barcodes(self):

        selected = self.product_tree.selection()
        barcode = None

        if selected:
            barcode = str(self.product_tree.item(selected[0])["values"][0])

        BarcodePrintDialog(
            self,
            selected_barcode=barcode,
        )

    # =====================================================
    # Search
    # =====================================================

    def create_searchbar(self):

        frame = tk.Frame(self.product_frame, bg="white")

        frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        tk.Label(
            frame,
            text="Search :",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).pack(side=tk.LEFT)

        self.search_var = tk.StringVar()

        entry = tk.Entry(
            frame,
            textvariable=self.search_var,
            width=35,
            font=("Segoe UI", 10),
        )

        entry.pack(side=tk.LEFT, padx=8)
        entry.focus()

        self.total_label = tk.StringVar()

        tk.Label(
            frame,
            textvariable=self.total_label,
            bg="white",
            fg="gray",
        ).pack(side=tk.RIGHT)

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh_table(),
        )

    # =====================================================
    # Product Table
    # =====================================================

    def create_table(self):

        columns = (
            "Barcode",
            "SKU",
            "Product Name",
            "Brand",
            "Category",
            "Stock",
            "Price",
            "GST",
        )

        # Separate container lets the Treeview shrink and grow
        # with the available window space.
        table_frame = tk.Frame(self.product_frame, bg="white")
        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
            pady=(0, 5),
        )

        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        self.product_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
        )
        self.product_tree.tag_configure("low_stock", foreground="#dc2626")
        self.product_tree.tag_configure("empty", foreground="#6b7280")

        widths = {
            "Barcode": 100,
            "SKU": 70,
            "Product Name": 180,
            "Brand": 100,
            "Category": 100,
            "Stock": 60,
            "Price": 80,
            "GST": 60,
        }

        for col in columns:
            self.product_tree.heading(col, text=col)
            
            stretch = True if col == "Product Name" else False
            
            self.product_tree.column(
                col,
                width=widths[col],
                anchor="center" if col != "Product Name" else "w",
                stretch=stretch,
            )

        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.product_tree.yview,
        )

        scroll_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.product_tree.xview,
        )

        self.product_tree.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        self.product_tree.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        scroll_y.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        scroll_x.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.product_tree.bind(
            "<Double-1>",
            self.on_double_click,
        )

    def on_double_click(self, event):
        if self.product_tree.identify_row(event.y):
            self.edit_product()

    # =====================================================
    # Toolbar Actions
    # =====================================================

    def add_product(self):
        AddProductDialog(
            self,
            refresh_callback=self.refresh_table,
        )

    def edit_product(self):

        selected = self.product_tree.selection()

        if not selected:

            messagebox.showwarning(
                "Edit Product",
                "Please select a product.",
            )

            return

        values = self.product_tree.item(selected[0])["values"]
        barcode = str(values[0])

        product = get_product_by_barcode(barcode)

        if not product:

            messagebox.showerror(
                "Error",
                "Product not found.",
            )

            return

        AddProductDialog(
            self,
            product=product,
            refresh_callback=self.refresh_table,
        )

    def delete_product(self):

        selected = self.product_tree.selection()

        if not selected:

            messagebox.showwarning(
                "Delete Product",
                "Please select a product.",
            )

            return

        values = self.product_tree.item(selected[0])["values"]

        barcode = str(values[0])
        name = values[2]

        if not messagebox.askyesno(
            "Delete Product",
            f"Delete '{name}' ?",
        ):
            return

        ok, msg = delete_product(barcode)

        if ok:
            self.refresh_table()
            self.product_tree.selection_remove(self.product_tree.selection())

            messagebox.showinfo(
                "Success",
                "Product deleted successfully.",
            )

        else:

            messagebox.showerror(
                "Error",
                msg,
            )

    # =====================================================
    # Load Products
    # =====================================================

    def refresh_table(self):

        self.product_tree.delete(*self.product_tree.get_children())

        keyword = self.search_var.get().strip()

        if keyword:
            products = search_products(keyword)
        else:
            products = get_all_products()

        self.total_label.set(f"Products : {len(products)}")

        if not products:
            if keyword:
                self.product_tree.insert("", tk.END, values=("", "", f"No products found for '{keyword}'", "", "", "", "", ""), tags=("empty",))
            else:
                self.product_tree.insert("", tk.END, values=("", "", "No products available.", "", "", "", "", ""), tags=("empty",))
            return

        for product in products:
            
            tags = ()
            if float(product.get("stock", 0)) <= float(product.get("min_stock", 0)):
                tags = ("low_stock",)

            self.product_tree.insert(
                "",
                tk.END,
                values=(
                    product.get("barcode", ""),
                    product.get("sku", ""),
                    product.get("name", ""),
                    product.get("brand", ""),
                    product.get("category", ""),
                    product.get("stock", 0),
                    f"₹ {float(product.get('selling_price', 0)):.2f}",
                    f"{product.get('gst', 0)} %",
                ),
                tags=tags,
            )

        children = self.product_tree.get_children()

        if children:
            self.product_tree.selection_set(children[0])