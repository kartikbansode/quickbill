import tkinter as tk
from tkinter import ttk
from gui.find_bill.bill_details_dialog import BillDetailsDialog


class FindBillView(tk.Frame):

    def __init__(self, parent, callbacks):

        super().__init__(parent, bg="#e9ecef")

        self.callbacks = callbacks

        self.bill_search_var = tk.StringVar()

        self.build_ui()

    def build_ui(self):

        # ==========================
        # Header
        # ==========================

        header = tk.Frame(self, bg="#e9ecef")
        header.pack(fill="x", padx=10, pady=10)

        tk.Label(
            header,
            text="Bill History",
            bg="#e9ecef",
            fg="#1f2937",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left")

        # ==========================
        # Search Section
        # ==========================

        search_frame = tk.LabelFrame(
            self,
            text="Search Invoice",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )

        search_frame.pack(fill="x", padx=10, pady=(0, 8))

        tk.Label(
            search_frame,
            text="Bill No / Customer / Mobile",
            bg="white",
            font=("Segoe UI", 10),
        ).grid(row=0, column=0, padx=10, pady=10)

        tk.Entry(
            search_frame,
            textvariable=self.bill_search_var,
            width=35,
            font=("Segoe UI", 10),
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            search_frame,
            text="Search",
            bg="#2563eb",
            fg="white",
            width=12,
            command=self.search_bill,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            search_frame,
            text="Refresh",
            bg="#16a34a",
            fg="white",
            width=12,
            command=self.refresh_table,
        ).grid(row=0, column=3, padx=5)

        # ==========================
        # Bill Table
        # ==========================

        table_frame = tk.Frame(self, bg="white")

        table_frame.pack(fill="both", expand=True, padx=10)

        columns = (
            "Bill No",
            "Date",
            "Payment",
            "Items",
            "Total",
        )

        self.bill_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=16,
        )

        widths = [180, 180, 120, 80, 120]

        for col, width in zip(columns, widths):

            self.bill_tree.heading(col, text=col)

            self.bill_tree.column(
                col,
                width=width,
                anchor="center",
            )

        scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.bill_tree.yview,
        )

        self.bill_tree.configure(
            yscrollcommand=scroll.set
        )

        self.bill_tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scroll.pack(
            side="right",
            fill="y",
        )

        # ==========================
        # Bottom Buttons
        # ==========================

        button_frame = tk.Frame(self, bg="#e9ecef")

        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            button_frame,
            text="View",
            width=14,
            bg="#2563eb",
            fg="white",
        ).pack(side="left")

        tk.Button(
            button_frame,
            text="Reprint",
            width=14,
            bg="#16a34a",
            fg="white",
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=14,
            bg="#dc2626",
            fg="white",
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Back",
            width=14,
            command=self.callbacks["back"],
        ).pack(side="right")

        self.bill_tree.bind(
        "<Double-1>",
        self.open_selected_bill,
        )

    def open_selected_bill(self, event=None):

        selected = self.bill_tree.selection()

        if not selected:

            return

        bill_no = self.bill_tree.item(selected[0])["values"][0]

        self.callbacks["view"](bill_no)

    def search_bill(self):

        if "search" in self.callbacks:

            self.callbacks["search"](
                self.bill_search_var.get().strip()
            )

    def refresh_table(self):

        if "refresh" in self.callbacks:

            self.callbacks["refresh"]()

    def clear_table(self):

        self.bill_tree.delete(*self.bill_tree.get_children())

    def add_bill(
        self,
        bill_no,
        date,
        payment,
        items,
        total,
    ):

        self.bill_tree.insert(
            "",
            "end",
            values=(
                bill_no,
                date,
                payment,
                items,
                total,
            ),
        )