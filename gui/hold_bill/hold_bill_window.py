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

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        width = min(980, int(screen_w * 0.9))
        height = min(680, int(screen_h * 0.9))
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.minsize(600, 400)
        self.resizable(True, True)

        self.resume_callback = resume_callback
        self._is_resuming = False

        self.build_ui()

        self.load_data()
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.tree.bind("<Double-1>", self.resume_bill)
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
        # ---------------- Header ----------------

        header = tk.Frame(self)

        header.pack(fill="x", padx=12, pady=(12, 5))

        tk.Label(
            header,
            text="Held Bills",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left")

        # ---------------- Search ----------------

        search_frame = tk.Frame(self)

        search_frame.pack(fill="x", padx=12, pady=(0, 10))

        tk.Label(
            search_frame,
            text="Search",
            font=("Segoe UI", 10),
        ).pack(side="left")

        self.search_var = tk.StringVar()

        self.search_var.trace_add(
            "write",
            lambda *_: self.load_data(),
        )

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            width=40,
        ).pack(side="left", padx=10)



        # ---------------- Table ----------------

        table_frame = tk.Frame(self)

        table_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 10),
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=18,
        )

        widths = [170, 130, 110, 90, 150, 120]

        for c, w in zip(columns, widths):

            self.tree.heading(c, text=c)

            self.tree.column(c, width=w, anchor="center")

        scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview,
        )

        self.tree.configure(
            yscrollcommand=scroll.set,
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scroll.pack(
            side="right",
            fill="y",
        )

        self.tree.focus_set()

        # ---------------- Bottom Buttons ----------------

        button_frame = tk.Frame(self)

        button_frame.pack(
            fill="x",
            padx=12,
            pady=(0, 12),
        )

        tk.Button(
            button_frame,
            text="▶ Resume Bill",
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=16,
            height=2,
            command=self.resume_bill,
        ).pack(side="left")

        tk.Button(
            button_frame,
            text="🗑 Delete Hold",
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            width=16,
            height=2,
            command=self.delete_bill,
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="⟳ Refresh",
            width=14,
            height=2,
            command=self.load_data,
        ).pack(side="right", padx=(10, 0))

        tk.Button(
            button_frame,
            text="✕ Close",
            width=14,
            height=2,
            command=self.destroy,
        ).pack(side="right")

    def load_data(self):

        self.tree.delete(*self.tree.get_children())

        bills = get_all_hold_bills()

        keyword = self.search_var.get().lower().strip()

        if keyword:

            bills = [bill for bill in bills if keyword in bill["hold_no"].lower()]

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
                ),
            )

    def resume_bill(self, event=None):

        if self._is_resuming:
            return

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning("Resume", "Please select a bill.")

            return

        self._is_resuming = True

        hold_no = self.tree.item(selected[0])["values"][0]

        bills = get_all_hold_bills()

        for bill in bills:

            if bill["hold_no"] == hold_no:

                self.resume_callback(bill)

                delete_hold_bill(hold_no)

                self.destroy()

                return
        
        self._is_resuming = False

    def delete_bill(self, event=None):

        selected = self.tree.selection()

        if not selected:

            return

        hold_no = self.tree.item(selected[0])["values"][0]

        if not messagebox.askyesno("Delete", f"Delete held bill '{hold_no}'?"):
            return

        delete_hold_bill(hold_no)

        self.load_data()

        children = self.tree.get_children()

        if children:

            self.tree.selection_set(children[0])

            self.tree.focus(children[0])
