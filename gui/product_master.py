import tkinter as tk
from tkinter import ttk, messagebox
from gui.ui_components import create_primary_button, create_success_button, create_warning_button, create_danger_button, create_secondary_button, ToolTip, FONT_LABEL, FONT_SECTION

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

        btn_add = create_success_button(self.toolbar_frame, "Add Product", command=self.add_product, width=14)
        btn_add.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(btn_add, "Add a new product")

        btn_edit = create_warning_button(self.toolbar_frame, "Edit Product", command=self.edit_product, width=14)
        btn_edit.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(btn_edit, "Edit selected product")

        btn_delete = create_danger_button(self.toolbar_frame, "Delete Product", command=self.delete_product, width=14)
        btn_delete.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(btn_delete, "Delete selected product")

        btn_print = create_primary_button(self.toolbar_frame, "Print Barcodes", command=self.print_barcodes, width=14)
        btn_print.pack(side=tk.LEFT, padx=(0, 8))
        ToolTip(btn_print, "Print barcodes for selected product")

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
        self.table_frame = tk.Frame(self.product_frame, bg="white")
        self.table_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=5,
            pady=(0, 5),
        )

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)
        
        self.empty_state_frame = tk.Frame(self.product_frame, bg="white")
        tk.Label(
            self.empty_state_frame,
            text="No products found. Add your first product to begin.",
            bg="white",
            fg="gray",
            font=("Segoe UI", 12)
        ).pack(pady=(50, 20))
        btn_add_empty = create_success_button(
            self.empty_state_frame,
            "Add Product",
            command=self.add_product,
            width=16
        )
        btn_add_empty.pack()

        self.product_tree = ttk.Treeview(
            self.table_frame,
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
            self.table_frame,
            orient="vertical",
            command=self.product_tree.yview,
        )

        scroll_x = ttk.Scrollbar(
            self.table_frame,
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
            self.table_frame.grid_remove()
            self.empty_state_frame.grid(row=1, column=0, sticky="nsew")
            return
            
        self.empty_state_frame.grid_remove()
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))

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