import tkinter as tk
from tkinter import ttk


class CartTable(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self._increase_callback = None
        self._decrease_callback = None
        self._delete_callback = None

        columns = ("S.No", "Barcode", "Product", "Qty", "Rate", "Amount")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=13)
        self.tree.heading("S.No", text="S.No")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Rate", text="Rate")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("S.No", width=60, anchor="center", stretch=False)
        self.tree.column("Barcode", width=140, anchor="center", stretch=False)
        self.tree.column("Product", width=340, stretch=True)
        self.tree.column("Qty", width=70, anchor="center", stretch=False)
        self.tree.column("Rate", width=90, anchor="center", stretch=False)
        self.tree.column("Amount", width=110, anchor="center", stretch=False)

        action_row = tk.Frame(self, bg="white")
        action_row.pack(side="bottom", fill="x", padx=6, pady=(0, 6))

        tk.Button(
            action_row,
            text="+ Qty",
            width=8,
            command=self.increase_quantity,
        ).pack(side="left", padx=2)

        tk.Button(
            action_row,
            text="- Qty",
            width=8,
            command=self.decrease_quantity,
        ).pack(side="left", padx=2)

        tk.Button(
            action_row,
            text="Delete",
            width=8,
            command=self.delete_item,
        ).pack(side="left", padx=2)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        self.empty_label = tk.Label(
            self,
            text="🛒\n\nCurrent Bill is Empty\n\nScan a barcode\nor\nType barcode manually and press Add",
            bg="white",
            fg="#808080",
            font=("Segoe UI", 12),
            justify="center",
        )
        self.tree.tag_configure("even", background="#FFFFFF")

        self.tree.tag_configure("odd", background="#F5F5F5")

        scrollbar.pack(side="right", fill="y")
        # Show empty message on startup
        self.tree.pack_forget()
        self.empty_label.pack(expand=True, fill="both")

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def set_actions(
        self, increase_callback=None, decrease_callback=None, delete_callback=None
    ):
        self._increase_callback = increase_callback
        self._decrease_callback = decrease_callback
        self._delete_callback = delete_callback

    def refresh_table(self, items):

        self.clear()

        if not items:

            self.tree.pack_forget()

            self.empty_label.pack(expand=True, fill="both")

            return

        self.empty_label.pack_forget()

        self.tree.pack(side="left", fill="both", expand=True)

        for index, item in enumerate(items):

            rate = item.get("selling_price", item.get("price", 0))

            tag = "even" if index % 2 == 0 else "odd"

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    index + 1,
                    item["barcode"],
                    item["name"],
                    item["qty"],
                    f"₹ {rate:.2f}",
                    f"₹ {item['total']:.2f}",
                ),
                tags=(tag,),
            )

    def add_item(self, barcode, product, qty, rate, amount):
        self.tree.insert("", "end", values=(barcode, product, qty, rate, amount))

    def selected(self):
        return self.tree.selection()

    def _selected_index(self):
        selection = self.selected()
        if not selection:
            return None
        try:
            return int(selection[0])
        except ValueError:
            return None

    def increase_quantity(self):
        index = self._selected_index()
        if index is not None and self._increase_callback:
            self._increase_callback(index)

    def decrease_quantity(self):
        index = self._selected_index()
        if index is not None and self._decrease_callback:
            self._decrease_callback(index)

    def delete_item(self):
        index = self._selected_index()
        if index is not None and self._delete_callback:
            self._delete_callback(index)
