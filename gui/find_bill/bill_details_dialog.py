import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

from logic.file_paths import data_path


class BillDetailsDialog(tk.Toplevel):

    def __init__(self, parent, bill):

        super().__init__(parent)

        self.parent = parent
        self.bill = bill

        self.title(
            f"Invoice Details - {bill.get('bill_no', '-')}"
        )

        self.width = 900
        self.height = 680

        x = (
            self.winfo_screenwidth()
            - self.width
        ) // 2

        y = (
            self.winfo_screenheight()
            - self.height
        ) // 2

        self.geometry(
            f"{self.width}x{self.height}+{x}+{y}"
        )

        self.minsize(
            820,
            600,
        )

        self.configure(
            bg="#e9ecef"
        )

        self.transient(parent)
        self.grab_set()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_dialog,
        )

        self.build_styles()
        self.build_ui()

        self.wait_visibility()
        self.focus_force()

        self.attributes(
            "-topmost",
            True,
        )

        self.after(
            100,
            lambda: self.attributes(
                "-topmost",
                False,
            ),
        )

    # =========================================================
    # Styles
    # =========================================================

    def build_styles(self):

        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Bill.Treeview",
            font=(
                "Segoe UI",
                9,
            ),
            rowheight=32,
            background="white",
            fieldbackground="white",
            foreground="#1f2937",
        )

        style.configure(
            "Bill.Treeview.Heading",
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
            background="#1f2937",
            foreground="white",
            padding=8,
        )

        style.map(
            "Bill.Treeview",
            background=[
                (
                    "selected",
                    "#dbeafe",
                )
            ],
            foreground=[
                (
                    "selected",
                    "#111827",
                )
            ],
        )

    # =========================================================
    # Main UI
    # =========================================================

    def build_ui(self):

        self.create_header()

        self.create_invoice_info()

        self.create_items_section()

        self.create_totals_section()

        self.create_action_bar()

    # =========================================================
    # Header
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self,
            bg="#1f2937",
            height=82,
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        left = tk.Frame(
            header,
            bg="#1f2937",
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
        )

        tk.Label(
            left,
            text="Invoice Details",
            bg="#1f2937",
            fg="white",
            font=(
                "Segoe UI",
                18,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(12, 0),
        )

        tk.Label(
            left,
            text="QuickBill Billing System",
            bg="#1f2937",
            fg="#cbd5e1",
            font=(
                "Segoe UI",
                9,
            ),
        ).pack(
            anchor="w",
        )

        status = self.bill.get(
            "status",
            "PAID",
        )

        status_frame = tk.Frame(
            header,
            bg="#166534",
        )

        status_frame.pack(
            side="right",
            padx=20,
            pady=22,
        )

        tk.Label(
            status_frame,
            text=str(status).upper(),
            bg="#166534",
            fg="white",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
            padx=16,
            pady=6,
        ).pack()

    # =========================================================
    # Invoice Information
    # =========================================================

    def create_invoice_info(self):

        outer = tk.Frame(
            self,
            bg="#e9ecef",
        )

        outer.pack(
            fill="x",
            padx=15,
            pady=12,
        )

        card = tk.Frame(
            outer,
            bg="white",
            bd=1,
            relief="solid",
        )

        card.pack(
            fill="x"
        )

        info = tk.Frame(
            card,
            bg="white",
        )

        info.pack(
            fill="x",
            padx=15,
            pady=12,
        )

        self.create_info_block(
            info,
            "BILL NUMBER",
            self.bill.get(
                "bill_no",
                "-",
            ),
            0,
        )

        self.create_info_block(
            info,
            "DATE & TIME",
            self.bill.get(
                "date",
                "-",
            ),
            1,
        )

        self.create_info_block(
            info,
            "PAYMENT METHOD",
            self.bill.get(
                "payment_mode",
                "-",
            ),
            2,
        )

        self.create_info_block(
            info,
            "CASHIER",
            self.bill.get(
                "cashier",
                "Admin",
            ),
            3,
        )

    def create_info_block(
        self,
        parent,
        label,
        value,
        column,
    ):

        block = tk.Frame(
            parent,
            bg="white",
        )

        block.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=8,
        )

        parent.grid_columnconfigure(
            column,
            weight=1,
        )

        tk.Label(
            block,
            text=label,
            bg="white",
            fg="#6b7280",
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
        ).pack(
            anchor="w"
        )

        tk.Label(
            block,
            text=str(value),
            bg="white",
            fg="#111827",
            font=(
                "Segoe UI",
                10,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

    # =========================================================
    # Items
    # =========================================================

    def create_items_section(self):

        section = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid",
        )

        section.pack(
            fill="both",
            expand=True,
            padx=15,
        )

        title_frame = tk.Frame(
            section,
            bg="white",
        )

        title_frame.pack(
            fill="x",
            padx=12,
            pady=(10, 6),
        )

        tk.Label(
            title_frame,
            text="Purchased Items",
            bg="white",
            fg="#111827",
            font=(
                "Segoe UI",
                11,
                "bold",
            ),
        ).pack(
            side="left"
        )

        items = self.bill.get(
            "items",
            [],
        )

        tk.Label(
            title_frame,
            text=f"{len(items)} item(s)",
            bg="white",
            fg="#6b7280",
            font=(
                "Segoe UI",
                9,
            ),
        ).pack(
            side="right"
        )

        table_frame = tk.Frame(
            section,
            bg="white",
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10),
        )

        columns = (
            "Item",
            "Barcode",
            "SKU",
            "Qty",
            "Rate",
            "GST",
            "Amount",
        )

        self.item_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Bill.Treeview",
        )

        widths = {
            "Item": 230,
            "Barcode": 120,
            "SKU": 90,
            "Qty": 60,
            "Rate": 100,
            "GST": 70,
            "Amount": 110,
        }

        for column in columns:

            self.item_tree.heading(
                column,
                text=column,
            )

            self.item_tree.column(
                column,
                width=widths[column],
                anchor="center",
            )

        self.item_tree.column(
            "Item",
            anchor="w",
        )

        self.item_tree.column(
            "Amount",
            anchor="e",
        )

        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.item_tree.yview,
        )

        scroll_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.item_tree.xview,
        )

        self.item_tree.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        self.item_tree.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scroll_y.pack(
            side="right",
            fill="y",
        )

        scroll_x.pack(
            side="bottom",
            fill="x",
        )

        for index, item in enumerate(
            items
        ):

            name = item.get(
                "name",
                "-",
            )

            barcode = item.get(
                "barcode",
                "-",
            )

            sku = item.get(
                "sku",
                "-",
            )

            qty = item.get(
                "qty",
                0,
            )

            price = self.safe_float(
                item.get(
                    "price",
                    item.get(
                        "selling_price",
                        0,
                    ),
                )
            )

            gst = item.get(
                "gst",
                "-",
            )

            total = self.safe_float(
                item.get(
                    "total",
                    price * self.safe_float(qty),
                )
            )

            tag = (
                "even"
                if index % 2 == 0
                else "odd"
            )

            self.item_tree.insert(
                "",
                "end",
                values=(
                    name,
                    barcode,
                    sku,
                    qty,
                    self.currency(
                        price
                    ),
                    f"{gst}%",
                    self.currency(
                        total
                    ),
                ),
                tags=(
                    tag,
                ),
            )

        self.item_tree.tag_configure(
            "even",
            background="#ffffff",
        )

        self.item_tree.tag_configure(
            "odd",
            background="#f8fafc",
        )

    # =========================================================
    # Totals
    # =========================================================

    def create_totals_section(self):

        outer = tk.Frame(
            self,
            bg="#e9ecef",
        )

        outer.pack(
            fill="x",
            padx=15,
            pady=10,
        )

        card = tk.Frame(
            outer,
            bg="white",
            bd=1,
            relief="solid",
        )

        card.pack(
            fill="x",
        )

        right = tk.Frame(
            card,
            bg="white",
        )

        right.pack(
            side="right",
            padx=18,
            pady=10,
        )

        self.create_total_row(
            right,
            "Subtotal",
            self.bill.get(
                "subtotal",
                0,
            ),
        )

        self.create_total_row(
            right,
            "Tax",
            self.bill.get(
                "tax",
                0,
            ),
        )

        self.create_total_row(
            right,
            "Discount",
            self.bill.get(
                "discount",
                0,
            ),
            negative=True,
        )

        separator = ttk.Separator(
            right,
            orient="horizontal",
        )

        separator.pack(
            fill="x",
            pady=5,
        )

        total_frame = tk.Frame(
            right,
            bg="white",
        )

        total_frame.pack(
            fill="x"
        )

        tk.Label(
            total_frame,
            text="GRAND TOTAL",
            bg="white",
            fg="#111827",
            font=(
                "Segoe UI",
                11,
                "bold",
            ),
        ).pack(
            side="left",
            padx=(0, 40),
        )

        tk.Label(
            total_frame,
            text=self.currency(
                self.bill.get(
                    "total",
                    0,
                )
            ),
            bg="white",
            fg="#15803d",
            font=(
                "Segoe UI",
                15,
                "bold",
            ),
        ).pack(
            side="right"
        )

        # Payment summary on left
        payment = tk.Frame(
            card,
            bg="#f8fafc",
        )

        payment.pack(
            side="left",
            fill="y",
            padx=18,
            pady=10,
        )

        tk.Label(
            payment,
            text="PAYMENT SUMMARY",
            bg="#f8fafc",
            fg="#6b7280",
            font=(
                "Segoe UI",
                8,
                "bold",
            ),
        ).pack(
            anchor="w",
            pady=(2, 5),
        )

        self.create_payment_row(
            payment,
            "Received",
            self.bill.get(
                "received_amount",
                self.bill.get(
                    "total",
                    0,
                ),
            ),
        )

        self.create_payment_row(
            payment,
            "Balance / Change",
            self.bill.get(
                "balance",
                0,
            ),
        )

    def create_total_row(
        self,
        parent,
        label,
        value,
        negative=False,
    ):

        frame = tk.Frame(
            parent,
            bg="white",
        )

        frame.pack(
            fill="x",
            pady=1,
        )

        tk.Label(
            frame,
            text=label,
            bg="white",
            fg="#6b7280",
            font=(
                "Segoe UI",
                9,
            ),
        ).pack(
            side="left",
            padx=(0, 45),
        )

        amount = self.currency(
            value
        )

        if negative:
            amount = f"- {amount}"

        tk.Label(
            frame,
            text=amount,
            bg="white",
            fg="#111827",
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
        ).pack(
            side="right"
        )

    def create_payment_row(
        self,
        parent,
        label,
        value,
    ):

        frame = tk.Frame(
            parent,
            bg="#f8fafc",
        )

        frame.pack(
            fill="x",
            pady=2,
        )

        tk.Label(
            frame,
            text=label,
            bg="#f8fafc",
            fg="#6b7280",
            font=(
                "Segoe UI",
                8,
            ),
        ).pack(
            side="left",
            padx=(0, 20),
        )

        tk.Label(
            frame,
            text=self.currency(
                value
            ),
            bg="#f8fafc",
            fg="#111827",
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
        ).pack(
            side="right"
        )

    # =========================================================
    # Action Bar
    # =========================================================

    def create_action_bar(self):

        bar = tk.Frame(
            self,
            bg="#e9ecef",
        )

        bar.pack(
            fill="x",
            padx=15,
            pady=(0, 12),
        )

        # Left buttons
        left = tk.Frame(
            bar,
            bg="#e9ecef",
        )

        left.pack(
            side="left"
        )

        self.create_button(
            left,
            "Open A4 PDF",
            "#2563eb",
            "#1d4ed8",
            self.open_a4_pdf,
        )

        self.create_button(
            left,
            "Open 80mm PDF",
            "#7c3aed",
            "#6d28d9",
            self.open_80mm_pdf,
        )

        self.create_button(
            left,
            "Reprint Both",
            "#16a34a",
            "#15803d",
            self.reprint,
        )

        self.create_button(
            left,
            "Open Bill Folder",
            "#475569",
            "#334155",
            self.open_bill_folder,
        )

        self.create_button(
            left,
            "Copy Bill No",
            "#64748b",
            "#475569",
            self.copy_bill_number,
        )

        # Close
        close_button = tk.Button(
            bar,
            text="Close",
            width=12,
            height=2,
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
            command=self.close_dialog,
        )

        close_button.pack(
            side="right"
        )

    # =========================================================
    # Button Helper
    # =========================================================

    def create_button(
        self,
        parent,
        text,
        bg,
        hover,
        command,
    ):

        button = tk.Button(
            parent,
            text=text,
            width=15,
            height=2,
            bg=bg,
            fg="white",
            activebackground=hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=(
                "Segoe UI",
                9,
                "bold",
            ),
            command=command,
        )

        button.pack(
            side="left",
            padx=(0, 6),
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(
                bg=hover
            ),
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(
                bg=bg
            ),
        )

        return button

    # =========================================================
    # PDF Paths
    # =========================================================

    def get_pdf_paths(self):

        bill_no = str(
            self.bill.get(
                "bill_no",
                "",
            )
        )

        bills_folder = data_path(
            "bills"
        )

        a4_path = os.path.join(
            bills_folder,
            f"{bill_no}_A4.pdf",
        )

        thermal_path = os.path.join(
            bills_folder,
            f"{bill_no}_80mm.pdf",
        )

        return (
            a4_path,
            thermal_path,
        )

    # =========================================================
    # Open A4
    # =========================================================

    def open_a4_pdf(self):

        a4_path, _ = (
            self.get_pdf_paths()
        )

        if not os.path.exists(
            a4_path
        ):

            self.regenerate_pdf(
                "A4 PDF is not available.\n\n"
                "Would you like to regenerate the invoice?"
            )

            return

        self.open_file(
            a4_path
        )

    # =========================================================
    # Open 80mm
    # =========================================================

    def open_80mm_pdf(self):

        _, thermal_path = (
            self.get_pdf_paths()
        )

        if not os.path.exists(
            thermal_path
        ):

            self.regenerate_pdf(
                "80mm PDF is not available.\n\n"
                "Would you like to regenerate the invoice?"
            )

            return

        self.open_file(
            thermal_path
        )

    # =========================================================
    # Reprint
    # =========================================================

    def reprint(self):

        try:

            from logic.pdf_generator import (
                generate_pdf_bill
            )

            result = generate_pdf_bill(
                self.bill["items"],
                self.bill["bill_no"],
                self.bill.get(
                    "payment_mode",
                    "Cash",
                ),
                self.bill.get(
                    "received_amount",
                    self.bill.get(
                        "total",
                        0,
                    ),
                ),
                cashier=self.bill.get(
                    "cashier",
                    "Admin",
                ),
                save_history=False,
            )

            messagebox.showinfo(
                "Reprint Successful",
                (
                    f"Invoice {self.bill['bill_no']} "
                    "has been regenerated.\n\n"
                    "A4 and 80mm PDFs are ready."
                ),
                parent=self,
            )

            # Open A4 after successful reprint
            if result.get("a4"):

                self.open_file(
                    result["a4"]
                )

        except Exception as e:

            messagebox.showerror(
                "Reprint Error",
                (
                    "Unable to regenerate "
                    "the invoice.\n\n"
                    f"{e}"
                ),
                parent=self,
            )

    # =========================================================
    # Regenerate Missing PDF
    # =========================================================

    def regenerate_pdf(
        self,
        message,
    ):

        answer = messagebox.askyesno(
            "PDF Not Found",
            message,
            parent=self,
        )

        if not answer:
            return

        try:

            from logic.pdf_generator import (
                generate_pdf_bill
            )

            result = generate_pdf_bill(
                self.bill["items"],
                self.bill["bill_no"],
                self.bill.get(
                    "payment_mode",
                    "Cash",
                ),
                self.bill.get(
                    "received_amount",
                    self.bill.get(
                        "total",
                        0,
                    ),
                ),
                cashier=self.bill.get(
                    "cashier",
                    "Admin",
                ),
                save_history=False,
            )

            messagebox.showinfo(
                "PDF Generated",
                "A4 and 80mm PDFs regenerated successfully.",
                parent=self,
            )

            if result.get("a4"):

                self.open_file(
                    result["a4"]
                )

        except Exception as e:

            messagebox.showerror(
                "PDF Error",
                f"Unable to generate PDF.\n\n{e}",
                parent=self,
            )

    # =========================================================
    # Open Bill Folder
    # =========================================================

    def open_bill_folder(self):

        folder = data_path(
            "bills"
        )

        os.makedirs(
            folder,
            exist_ok=True,
        )

        try:

            os.startfile(
                folder
            )

        except AttributeError:

            subprocess.Popen(
                [
                    "xdg-open",
                    folder,
                ]
            )

        except Exception as e:

            messagebox.showerror(
                "Folder Error",
                f"Unable to open bill folder.\n\n{e}",
                parent=self,
            )

    # =========================================================
    # Copy Bill Number
    # =========================================================

    def copy_bill_number(self):

        bill_no = str(
            self.bill.get(
                "bill_no",
                "",
            )
        )

        self.clipboard_clear()
        self.clipboard_append(
            bill_no
        )
        self.update()

        messagebox.showinfo(
            "Copied",
            f"Bill number {bill_no} copied to clipboard.",
            parent=self,
        )

    # =========================================================
    # File Open Helper
    # =========================================================

    def open_file(
        self,
        path,
    ):

        if not os.path.exists(
            path
        ):

            messagebox.showerror(
                "File Not Found",
                f"PDF file was not found:\n\n{path}",
                parent=self,
            )

            return

        try:

            os.startfile(
                path
            )

        except Exception as e:

            messagebox.showerror(
                "Open PDF Error",
                f"Unable to open PDF.\n\n{e}",
                parent=self,
            )

    # =========================================================
    # Currency
    # =========================================================

    def currency(
        self,
        value,
    ):

        try:

            amount = float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            amount = 0.0

        return f"₹ {amount:,.2f}"

    # =========================================================
    # Safe Float
    # =========================================================

    def safe_float(
        self,
        value,
    ):

        try:

            return float(
                value
            )

        except (
            TypeError,
            ValueError,
        ):

            return 0.0

    # =========================================================
    # Close
    # =========================================================

    def close_dialog(self):

        try:

            self.grab_release()

        except Exception:
            pass

        self.destroy()