import tkinter as tk
from datetime import datetime
from gui.ui_components import BG_STATUSBAR, TEXT_MUTED, SUCCESS, DANGER


class StatusBar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg=BG_STATUSBAR, height=30)

        self.pack_propagate(False)

        self.status = tk.StringVar(value="Ready")
        self.scanner = tk.StringVar(value="Connected")
        self.operator = tk.StringVar(value="Admin")
        self.bill_no = tk.StringVar(value="QB-000001")
        self.datetime = tk.StringVar()
        self.version = tk.StringVar(value="QuickBill Pro v2.2.0")
        
        self.status_color = tk.StringVar(value="white")
        self.scanner_color = tk.StringVar(value=SUCCESS)

        self._add_label("Status")
        self.status_label = tk.Label(
            self,
            textvariable=self.status,
            bg=BG_STATUSBAR,
            fg="white",
            font=("Segoe UI", 9, "bold"),
        )
        self.status_label.pack(side="left")

        self._separator()

        self._add_label("Scanner")
        self.scanner_label = tk.Label(
            self,
            textvariable=self.scanner,
            bg=BG_STATUSBAR,
            fg=SUCCESS,
            font=("Segoe UI", 9, "bold"),
        )
        self.scanner_label.pack(side="left")

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
            bg=BG_STATUSBAR,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9),
        ).pack(side="left", padx=(10, 2))

    def _add_value(self, var, color="white"):
        tk.Label(
            self,
            textvariable=var,
            bg=BG_STATUSBAR,
            fg=color,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left")

    def _separator(self):
        tk.Label(
            self,
            text="|",
            bg=BG_STATUSBAR,
            fg="#4b5563",
        ).pack(side="left", padx=8)


    def set_bill_number(self, bill):
        self.bill_no.set(bill)

    def set_status(self, text, timeout=None):
        self.status.set(text)
        self.status_label.config(fg="white")
        if hasattr(self, '_status_timer'):
            self.after_cancel(self._status_timer)
        if timeout:
            self._status_timer = self.after(timeout, lambda: self.status.set("Ready"))
            
    def set_temporary_status(self, message, duration_ms=3000):
        self.status.set(message)
        self.status_label.config(fg=SUCCESS)
        if hasattr(self, '_status_timer'):
            self.after_cancel(self._status_timer)
        self._status_timer = self.after(duration_ms, lambda: self._revert_status())

    def _revert_status(self):
        self.status.set("Ready")
        self.status_label.config(fg="white")

    def scanner_connected(self):
        self.scanner.set("Connected")
        self.scanner_label.config(fg=SUCCESS)

    def scanner_disconnected(self):
        self.scanner.set("Disconnected")
        self.scanner_label.config(fg=DANGER)

    def set_operator(self, name):
        self.operator.set(name)