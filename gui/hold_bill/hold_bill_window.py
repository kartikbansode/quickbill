import tkinter as tk
from tkinter import ttk, messagebox

from logic.hold_bill import (
    get_all_hold_bills,
    delete_hold_bill,
)


class HoldBillWindow(tk.Toplevel):

    def __init__(self, parent, resume_callback):

        super().__init__(parent)

        self.title("Held Bills")

        self.geometry("850x450")

        self.resizable(False, False)

        self.resume_callback = resume_callback

        self.build_ui()

        self.load_data()
        self.tree.bind("<Double-1>", lambda e: self.resume_bill())
        self.bind("<Return>", lambda e: self.resume_bill())

        self.bind("<Delete>", lambda e: self.delete_bill())

        self.bind("<Escape>", lambda e: self.destroy())

    def build_ui(self):

        columns = (
            "Hold No",
            "Date",
            "Time",
            "Items",
            "Amount",
            "Cashier",
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=14,
        )

        widths = [120,120,100,80,120,100]

        for c, w in zip(columns, widths):

            self.tree.heading(c, text=c)

            self.tree.column(c, width=w, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        button_frame = tk.Frame(self)

        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            button_frame,
            text="Resume Bill",
            bg="#16a34a",
            fg="white",
            width=15,
            command=self.resume_bill,
        ).pack(side="left")

        tk.Button(
            button_frame,
            text="Delete Hold",
            bg="#dc2626",
            fg="white",
            width=15,
            command=self.delete_bill,
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Close",
            width=15,
            command=self.destroy,
        ).pack(side="right")

    def load_data(self):

        self.tree.delete(*self.tree.get_children())

        bills = get_all_hold_bills()

        bills.reverse()

        for bill in bills:

            amount = sum(item["total"] for item in bill["cart"])

            self.tree.insert(
                "",
                "end",
                values=(
                bill["hold_no"],
                bill["date"],
                bill["time"],
                sum(item["qty"] for item in bill["cart"]),
                f"₹ {amount:.2f}",
                bill.get("cashier", "Admin"),
                )
            )

        def resume_bill(self):

            selected = self.tree.selection()

            if not selected:

                messagebox.showwarning("Resume", "Please select a bill.")

                return

            hold_no = self.tree.item(selected[0])["values"][0]

            bills = get_all_hold_bills()

            for bill in bills:

                if bill["hold_no"] == hold_no:

                    self.resume_callback(bill)

                    delete_hold_bill(hold_no)

                    self.destroy()

                    return

        def delete_bill(self):

            selected = self.tree.selection()

            if not selected:

                return

            hold_no = self.tree.item(selected[0])["values"][0]

            if not messagebox.askyesno("Delete", "Delete this held bill?"):
                return

            delete_hold_bill(hold_no)

            self.load_data()
