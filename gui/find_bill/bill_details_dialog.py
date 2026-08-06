import tkinter as tk
from tkinter import ttk


class BillDetailsDialog(tk.Toplevel):

    def __init__(self, parent, bill):

        super().__init__(parent)

        self.title(f"Invoice - {bill['bill_no']}")

        width = 700
        height = 500

        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.resizable(False, False)

        self.bill = bill

        self.build_ui()
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

    def close_dialog(self):

        self.grab_release()

        self.destroy()

    def build_ui(self):

        tk.Label(
            self,
            text=f"Invoice : {self.bill['bill_no']}",
            font=("Segoe UI", 15, "bold"),
        ).pack(pady=10)

        info = tk.Frame(self)

        info.pack(fill="x", padx=20)

        tk.Label(
            info,
            text=f"Date : {self.bill['date']}",
        ).pack(anchor="w")

        tk.Label(
            info,
            text=f"Payment : {self.bill.get('payment_mode','-')}",
        ).pack(anchor="w")

        tk.Label(
            info,
            text=f"Total : ₹ {self.bill['total']:.2f}",
        ).pack(anchor="w")

        columns = (
            "Item",
            "Qty",
            "Price",
            "Total",
        )

        tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=15,
        )

        for c in columns:

            tree.heading(c, text=c)

            tree.column(c, anchor="center")

        tree.pack(fill="both", expand=True, padx=15, pady=10)

        for item in self.bill["items"]:

            tree.insert(
                "",
                "end",
                values=(
                    item["name"],
                    item["qty"],
                    f"₹ {item['price']:.2f}",
                    f"₹ {item['total']:.2f}",
                ),
            )
