import tkinter as tk
from logic.database import get_all_products
from tkinter import ttk
from gui.ui_components import create_success_button, create_secondary_button, show_error, FONT_LABEL, FONT_INPUT, FONT_SECTION
from logic.database import (
    add_product,
    edit_product,
    get_all_products,
)


class AddProductDialog:

    def __init__(self, parent, refresh_callback=None, product=None):

        self.refresh_callback = refresh_callback

        self.product = product

        self.window = tk.Toplevel(parent)

        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_force()

        if product:

            self.window.title("Edit Product")

        else:

            self.window.title("Add Product")

        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()

        width = min(800, int(screen_w * 0.9))
        height = min(700, int(screen_h * 0.9))

        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.window.minsize(600, 500)
        self.window.resizable(True, True)

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close_dialog,
        )

        self.entries = {}

        # Allow Esc to close
        self.window.bind("<Escape>", lambda e: self.close_dialog())

        self.build_ui()

        if product:
            self.load_product()
            self.entries["Product Name"].focus_set()
        else:
            self.generate_barcode()

            self.entries["Product Name"].focus_set()

    def close_dialog(self):
        self.window.grab_release()
        self.window.destroy()

    def load_product(self):

        self.entries["Barcode"].config(state="normal")

        for key, widget in self.entries.items():

            value = ""

            if key == "Barcode":
                value = self.product.get("barcode", "")

            elif key == "Product Name":
                value = self.product.get("name", "")

            elif key == "Brand":
                value = self.product.get("brand", "")

            elif key == "Category":
                value = self.product.get("category", "")

            elif key == "Purchase Price":
                value = self.product.get("purchase_price", "")

            elif key == "Selling Price":
                value = self.product.get("selling_price", "")

            elif key == "MRP":
                value = self.product.get("mrp", "")

            elif key == "GST":
                value = self.product.get("gst", "")

            elif key == "Opening Stock":
                value = self.product.get("stock", "")

            elif key == "Minimum Stock":
                value = self.product.get("min_stock", "")

            elif key == "Supplier":
                value = self.product.get("supplier", "")

            elif key == "Unit":
                value = self.product.get("unit", "")

            elif key == "Weight":
                value = self.product.get("weight", "")

            elif key == "Description":
                value = self.product.get("description", "")

            widget.delete(0, tk.END)

            widget.insert(0, str(value))

        self.entries["Barcode"].config(state="readonly")

    def generate_barcode(self):

        products = get_all_products()

        highest = 1000000000

        for product in products:

            try:

                number = int(product["barcode"])

                if number > highest:

                    highest = number

            except:

                pass

        new_barcode = str(highest + 1)

        barcode_entry = self.entries["Barcode"]

        barcode_entry.delete(0, tk.END)

        barcode_entry.insert(0, new_barcode)

        barcode_entry.config(state="readonly")

    def build_ui(self):

        title_text = "Edit Product" if self.product else "Add New Product"

        title = tk.Label(
            self.window,
            text=title_text,
            font=("Segoe UI", 16, "bold"),
        )

        title.pack(pady=15)

        form = tk.Frame(self.window)

        form.pack(fill="both", expand=True, padx=25)

        left_fields = [
            "Barcode",
            "Product Name",
            "Brand",
            "Category",
            "Purchase Price",
            "Selling Price",
            "MRP",
        ]

        right_fields = [
            "GST",
            "Opening Stock",
            "Minimum Stock",
            "Supplier",
            "Unit",
            "Weight",
            "Description",
        ]

        for row in range(max(len(left_fields), len(right_fields))):
            if row < len(left_fields):
                field = left_fields[row]
                tk.Label(
                    form, text=field, width=18, anchor="w", font=("Segoe UI", 10)
                ).grid(row=row, column=0, padx=10, pady=6, sticky="w")
    
                if field == "Category":
                    entry = ttk.Combobox(
                        form,
                        width=30,
                        state="readonly",
                        values=[
                            "Snacks",
                            "Beverages",
                            "Dairy",
                            "Bakery",
                            "Groceries",
                            "Household",
                            "Stationery",
                            "Others",
                        ],
                    )
                    entry.current(0)
                else:
                    entry = tk.Entry(form, width=33)
    
                entry.grid(row=row, column=1, pady=6)
                self.entries[field] = entry

            if row < len(right_fields):
                field = right_fields[row]
                tk.Label(
                    form, text=field, width=18, anchor="w", font=("Segoe UI", 10)
                ).grid(row=row, column=2, padx=(30, 10), pady=6, sticky="w")
    
                if field == "GST":
                    entry = ttk.Combobox(
                        form,
                        width=30,
                        state="readonly",
                        values=["0", "5", "12", "18", "28"],
                    )
                    entry.current(3)
                elif field == "Unit":
                    entry = ttk.Combobox(
                        form,
                        width=30,
                        state="readonly",
                        values=["Piece", "Packet", "Bottle", "Kg", "Gram", "Litre"],
                    )
                    entry.current(0)
                else:
                    entry = tk.Entry(form, width=33)
    
                entry.grid(row=row, column=3, pady=6)
                self.entries[field] = entry

        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=20)
        
        btn_save = create_success_button(
            btn_frame,
            "Save Product",
            command=self.save_product,
            width=18
        )
        btn_save.pack(side="left", padx=10)
        
        btn_cancel = create_secondary_button(
            btn_frame,
            "Cancel",
            command=self.close_dialog,
            width=12
        )
        btn_cancel.pack(side="left", padx=10)

    def save_product(self):

        barcode = self.entries["Barcode"].get()

        name = self.entries["Product Name"].get().strip()

        if name == "":

            show_error(self.window, "Error", "Product Name is required.")

            return

        try:

            purchase_price = float(self.entries["Purchase Price"].get())

            selling_price = float(self.entries["Selling Price"].get())

            mrp = float(self.entries["MRP"].get())

            gst = int(self.entries["GST"].get())

            stock = int(self.entries["Opening Stock"].get() or 0)

            min_stock = int(self.entries["Minimum Stock"].get() or 0)

        except ValueError:

            show_error(
                self.window,
                "Invalid Input",
                "Please enter valid numeric values for Price, GST and Stock.",
            )

            return

        product = {
            "barcode": barcode,
            "sku": (
                self.product["sku"]
                if self.product
                else f"SKU{len(get_all_products())+1:04d}"
            ),
            "name": name,
            "brand": self.entries["Brand"].get(),
            "category": self.entries["Category"].get(),
            "purchase_price": purchase_price,
            "selling_price": selling_price,
            "mrp": mrp,
            "gst": gst,
            "stock": stock,
            "min_stock": min_stock,
            "supplier": self.entries["Supplier"].get(),
            "unit": self.entries["Unit"].get(),
            "weight": self.entries["Weight"].get(),
            "expiry": "",
            "batch": "",
            "hsn": "",
            "description": self.entries["Description"].get(),
        }

        if self.product:

            ok, msg = edit_product(barcode, product)

            success_message = "Product Updated Successfully."

        else:

            ok, msg = add_product(barcode, product)

            success_message = "Product Added Successfully."

        if ok:

            self.close_dialog()

            if self.refresh_callback:
                self.refresh_callback()

        else:

            show_error(self.window, "Error", msg)
