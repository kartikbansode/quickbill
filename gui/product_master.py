import tkinter as tk
from tkinter import ttk, messagebox

from logic.database import add_product, edit_product, delete_product, get_all_products


class ProductMaster(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent, bg="#f4f6f9")

        self.create_ui()

        self.load_products()

    def create_ui(self):

        title = tk.Label(
            self, text="Product Master", font=("Segoe UI", 18, "bold"), bg="#f4f6f9"
        )

        title.pack(anchor="w", padx=15, pady=10)

        self.table = ttk.Treeview(
            self,
            columns=("Barcode", "SKU", "Name", "Brand", "Category", "Stock", "Price"),
            show="headings",
            height=14,
        )

        widths = [130, 90, 220, 120, 120, 80, 80]

        for c, w in zip(self.table["columns"], widths):

            self.table.heading(c, text=c)

            self.table.column(c, width=w)

        # ---------- Toolbar ----------

        toolbar = tk.Frame(self, bg="#f4f6f9")
        toolbar.pack(fill="x", padx=15, pady=(0, 8))

        tk.Button(
            toolbar,
            text="+ Add Product",
            bg="#28a745",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            width=15,
            command=self.add_product_window,
        ).pack(side="left")

        tk.Button(toolbar, text="Edit", width=10, command=self.edit_selected).pack(
            side="left", padx=5
        )

        tk.Button(toolbar, text="Delete", width=10, command=self.delete_selected).pack(
            side="left"
        )

        table_frame = tk.Frame(self, bg="#f4f6f9")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.table.pack(in_=table_frame, side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )

        scrollbar.pack(side="right", fill="y")

        self.table.configure(yscrollcommand=scrollbar.set)

    def add_product_window(self):
        pass

    def edit_selected(self):
        messagebox.showinfo("Coming Soon", "Edit Product")

    def delete_selected(self):
        messagebox.showinfo("Coming Soon", "Delete Product")

    def load_products(self):

        self.table.delete(*self.table.get_children())

        for p in get_all_products():

            self.table.insert(
                "",
                "end",
                values=(
                    p["barcode"],
                    p["sku"],
                    p["name"],
                    p["brand"],
                    p["category"],
                    p["stock"],
                    p["selling_price"],
                ),
            )
