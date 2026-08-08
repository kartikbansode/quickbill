import tkinter as tk
from tkinter import ttk


class FindBillView(tk.Frame):

    def __init__(self, parent, callbacks):

        super().__init__(
            parent,
            bg="#e9ecef",
        )

        self.callbacks = callbacks

        self.bill_search_var = tk.StringVar()

        self.build_ui()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        # =================================================
        # Header
        # =================================================

        header = tk.Frame(
            self,
            bg="#e9ecef",
        )

        header.pack(
            fill="x",
            padx=10,
            pady=10,
        )

        tk.Label(
            header,
            text="Bill History",
            bg="#e9ecef",
            fg="#1f2937",
            font=("Segoe UI", 18, "bold"),
        ).pack(
            side="left"
        )

        # =================================================
        # Search Section
        # =================================================

        search_frame = tk.LabelFrame(
            self,
            text="Search Invoice",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        )

        search_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 8),
        )

        tk.Label(
            search_frame,
            text="Bill No / Payment / Date",
            bg="white",
            font=("Segoe UI", 10),
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
        )

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.bill_search_var,
            width=35,
            font=("Segoe UI", 10),
        )

        search_entry.grid(
            row=0,
            column=1,
            padx=5,
        )

        search_entry.focus_set()

        tk.Button(
            search_frame,
            text="Search",
            bg="#2563eb",
            fg="white",
            width=12,
            command=self.search_bill,
        ).grid(
            row=0,
            column=2,
            padx=5,
        )

        tk.Button(
            search_frame,
            text="Refresh",
            bg="#16a34a",
            fg="white",
            width=12,
            command=self.refresh_table,
        ).grid(
            row=0,
            column=3,
            padx=5,
        )

        # =================================================
        # Bill Table
        # =================================================

        table_frame = tk.Frame(
            self,
            bg="white",
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
        )

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

        widths = {
            "Bill No": 180,
            "Date": 180,
            "Payment": 120,
            "Items": 80,
            "Total": 120,
        }

        for col in columns:

            self.bill_tree.heading(
                col,
                text=col,
            )

            self.bill_tree.column(
                col,
                width=widths[col],
                anchor="center",
            )

        # Total should remain readable
        self.bill_tree.column(
            "Total",
            anchor="e",
        )

        scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.bill_tree.yview,
        )

        self.bill_tree.configure(
            yscrollcommand=scroll.set,
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

        # =================================================
        # Bottom Buttons
        # =================================================

        button_frame = tk.Frame(
            self,
            bg="#e9ecef",
        )

        button_frame.pack(
            fill="x",
            padx=10,
            pady=10,
        )

        tk.Button(
            button_frame,
            text="View",
            width=14,
            bg="#2563eb",
            fg="white",
            command=self.open_selected_bill,
        ).pack(
            side="left",
        )

        tk.Button(
            button_frame,
            text="Reprint",
            width=14,
            bg="#16a34a",
            fg="white",
            command=self.reprint_selected_bill,
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            button_frame,
            text="Delete",
            width=14,
            bg="#dc2626",
            fg="white",
            command=self.delete_selected_bill,
        ).pack(
            side="left",
            padx=5,
        )

        tk.Button(
            button_frame,
            text="Back",
            width=14,
            command=self.callbacks["back"],
        ).pack(
            side="right",
        )

        self.bill_tree.bind(
            "<Double-1>",
            self.on_double_click,
        )

    # =====================================================
    # Double Click
    # =====================================================

    def on_double_click(self, event):

        if self.bill_tree.identify_row(event.y):

            self.open_selected_bill()

    # =====================================================
    # Delete
    # =====================================================

    def delete_selected_bill(self):

        selected = self.bill_tree.selection()

        if not selected:
            return

        bill_no = self.bill_tree.item(
            selected[0]
        )["values"][0]

        if "delete" in self.callbacks:

            self.callbacks["delete"](
                bill_no
            )

    # =====================================================
    # Reprint
    # =====================================================

    def reprint_selected_bill(self):

        selected = self.bill_tree.selection()

        if not selected:
            return

        bill_no = self.bill_tree.item(
            selected[0]
        )["values"][0]

        if "reprint" in self.callbacks:

            self.callbacks["reprint"](
                bill_no
            )

    # =====================================================
    # View
    # =====================================================

    def open_selected_bill(
        self,
        event=None,
    ):

        selected = self.bill_tree.selection()

        if not selected:
            return

        bill_no = self.bill_tree.item(
            selected[0]
        )["values"][0]

        self.callbacks["view"](
            bill_no
        )

    # =====================================================
    # Search
    # =====================================================

    def search_bill(self):

        if "search" in self.callbacks:

            self.callbacks["search"](
                self.bill_search_var.get().strip()
            )

    # =====================================================
    # Refresh
    # =====================================================

    def refresh_table(self):

        if "refresh" in self.callbacks:

            self.callbacks["refresh"]()

    # =====================================================
    # Clear
    # =====================================================

    def clear_table(self):

        self.bill_tree.delete(
            *self.bill_tree.get_children()
        )

    # =====================================================
    # Add Bill
    # =====================================================

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