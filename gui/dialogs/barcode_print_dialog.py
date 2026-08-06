import os
import webbrowser
import tkinter as tk

from tkinter import ttk, messagebox

from logic.database import (
    get_all_products,
    get_product_by_barcode,
)

from logic.barcode_pdf import generate_barcode_pdf


class BarcodePrintDialog(tk.Toplevel):

    def __init__(self, parent, selected_barcode=None):

        super().__init__(parent)

        self.title("Print Barcode Labels")

        width = 650
        height = 600

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()
        self.wait_visibility()
        self.focus_force()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_dialog,
        )

        self.attributes("-topmost", True)
        self.after(
            100,
            lambda: self.attributes("-topmost", False),
        )

        self.mode = tk.StringVar(value="selected")
        self.selected_barcode = selected_barcode

        self.show_name = tk.BooleanVar(value=True)
        self.show_price = tk.BooleanVar(value=True)
        self.show_number = tk.BooleanVar(value=True)
        self.layout_var = tk.StringVar(value="10")

        self.columns_var = tk.IntVar(value=2)

        self.rows_var = tk.IntVar(value=5)

        self.build_ui()

    def close_dialog(self):

        self.grab_release()
        self.destroy()

    def build_ui(self):

        title = tk.Label(
            self,
            text="Print Barcode Labels",
            font=("Segoe UI", 18, "bold"),
        )

        title.pack(pady=15)

        options = tk.LabelFrame(
            self,
            text="Select Products",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=15,
        )

        options.pack(fill="x", padx=20)

        tk.Radiobutton(
            options,
            text="Selected Product",
            variable=self.mode,
            value="selected",
        ).pack(anchor="w")

        tk.Radiobutton(
            options,
            text="All Products",
            variable=self.mode,
            value="all",
        ).pack(anchor="w")

        tk.Radiobutton(
            options,
            text="Barcode Range",
            variable=self.mode,
            value="range",
        ).pack(anchor="w")

        range_frame = tk.Frame(options)

        range_frame.pack(fill="x", pady=5)

        tk.Label(
            range_frame,
            text="From",
            width=8,
        ).grid(row=0, column=0)

        self.from_entry = tk.Entry(range_frame, width=20)

        self.from_entry.grid(row=0, column=1)

        tk.Label(
            range_frame,
            text="To",
            width=8,
        ).grid(row=0, column=2)

        self.to_entry = tk.Entry(range_frame, width=20)

        self.to_entry.grid(row=0, column=3)

        layout = tk.LabelFrame(
            self,
            text="Label Options",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=15,
        )

        layout.pack(fill="x", padx=20, pady=10)

        tk.Checkbutton(
            layout,
            text="Show Product Name",
            variable=self.show_name,
        ).pack(anchor="w")

        tk.Checkbutton(
            layout,
            text="Show Price",
            variable=self.show_price,
        ).pack(anchor="w")

        tk.Checkbutton(
            layout,
            text="Show Barcode Number",
            variable=self.show_number,
        ).pack(anchor="w")

        layout_frame = tk.LabelFrame(
            self,
            text="Layout",
            font=("Segoe UI", 10, "bold"),
        )

        layout_frame.pack(fill="x", padx=15, pady=8)

        bottom = tk.Frame(self)

        bottom.pack(fill="x", pady=20)

        tk.Button(
            bottom,
            text="Generate PDF",
            width=18,
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.generate_pdf,
        ).pack(side="left", padx=20)

        tk.Button(
            bottom,
            text="Cancel",
            width=16,
            command=self.close_dialog,
        ).pack(side="right", padx=20)

        tk.Label(
            layout_frame,
            text="Labels Per Page",
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        layout_combo = ttk.Combobox(
            layout_frame,
            width=18,
            state="readonly",
            textvariable=self.layout_var,
            values=[
                "10",
                "12",
                "14",
                "24",
                "30",
                "Custom",
            ],
        )

        layout_combo.grid(
            row=0,
            column=1,
            padx=10,
        )

        layout_combo.bind(
            "<<ComboboxSelected>>",
            self.layout_changed,
        )

        tk.Label(
            layout_frame,
            text="Columns",
            bg="white",
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        tk.Spinbox(
            layout_frame,
            from_=1,
            to=5,
            width=5,
            textvariable=self.columns_var,
        ).grid(row=1, column=1, sticky="w")

        tk.Label(
            layout_frame,
            text="Rows",
            bg="white",
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        tk.Spinbox(
            layout_frame,
            from_=1,
            to=15,
            width=5,
            textvariable=self.rows_var,
        ).grid(row=2, column=1, sticky="w")

        self.from_entry.focus_set()

    def layout_changed(self, event=None):

        value = self.layout_var.get()

        presets = {
            "10": (2, 5),
            "12": (2, 6),
            "14": (2, 7),
            "24": (3, 8),
            "30": (3, 10),
        }

        if value in presets:

            c, r = presets[value]

            self.columns_var.set(c)

            self.rows_var.set(r)

    def preview_pdf(self):

        pdf = self.generate_pdf()

        if pdf:
            webbrowser.open(pdf)

    def generate_pdf(self):

        mode = self.mode.get()

        products = []

        if mode == "selected":

            if not self.selected_barcode:

                messagebox.showwarning(
                    "No Product",
                    "Please select a product first.",
                )
                return

            product = get_product_by_barcode(self.selected_barcode)

            if product:
                products.append(product)

        elif mode == "all":

            products = get_all_products()

        else:

            start = self.from_entry.get().strip()

            end = self.to_entry.get().strip()

            if not start or not end:

                messagebox.showwarning(
                    "Barcode Range",
                    "Enter both barcode values.",
                )

                return

            for product in get_all_products():

                barcode = str(product["barcode"])

                if start <= barcode <= end:

                    products.append(product)

        if not products:

            messagebox.showwarning(
                "No Products",
                "Nothing to print.",
            )

            return

        pdf = generate_barcode_pdf(
            products,
            show_name=self.show_name.get(),
            show_price=self.show_price.get(),
            show_number=self.show_number.get(),
            columns=self.columns_var.get(),
            rows=self.rows_var.get(),
        )

        webbrowser.open(pdf)

        messagebox.showinfo(
            "Success",
            "Barcode PDF generated successfully.",
        )

        self.close_dialog()

        return pdf
