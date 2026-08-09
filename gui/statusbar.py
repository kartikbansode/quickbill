import tkinter as tk
from datetime import datetime


class StatusBar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#1f2937", height=30)

        self.pack_propagate(False)

        self.status = tk.StringVar(value="Ready")
        self.scanner = tk.StringVar(value="Connected")
        self.operator = tk.StringVar(value="Admin")
        self.bill_no = tk.StringVar(value="QB-000001")
        self.datetime = tk.StringVar()
        self.version = tk.StringVar(value="QuickBill Pro v2.2.0")

        self._add_label("Status")
        self._add_value(self.status)

        self._separator()

        self._add_label("Scanner")
        self._add_value(self.scanner, "#22c55e")

        self._separator()

        self._add_label("Operator")
        self._add_value(self.operator)

        self._separator()

        self._add_label("Bill")
        self._add_value(self.bill_no)

        self._separator()

   


    def _add_label(self, text):
        tk.Label(
            self,
            text=f"{text}:",
            bg="#1f2937",
            fg="#9ca3af",
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(10, 2))

    def _add_value(self, var, color="white"):
        tk.Label(
            self,
            textvariable=var,
            bg="#1f2937",
            fg=color,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

    def _separator(self):
        tk.Label(
            self,
            text="|",
            bg="#1f2937",
            fg="#4b5563",
        ).pack(side="left", padx=8)


    def set_bill_number(self, bill):
        self.bill_no.set(bill)

    def set_status(self, text):
        self.status.set(text)

    def scanner_connected(self):
        self.scanner.set("Connected")

    def scanner_disconnected(self):
        self.scanner.set("Disconnected")

    def set_operator(self, name):
        self.operator.set(name)