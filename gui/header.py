import tkinter as tk
import datetime


class Header(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1d3557", height=80)

        self.pack_propagate(False)

        left = tk.Frame(self, bg="#1d3557")
        left.pack(side="left", padx=15)

        tk.Label(
            left,
            text="QuickBill Pro",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#1d3557",
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Professional Billing Software",
            font=("Segoe UI", 9),
            fg="#d0d0d0",
            bg="#1d3557",
        ).pack(anchor="w")

        right = tk.Frame(self, bg="#1d3557")
        right.pack(side="right", padx=15)

        self.time_label = tk.Label(
            right,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg="white",
            bg="#1d3557",
        )
        self.time_label.pack(anchor="e")

        self.date_label = tk.Label(
            right,
            text="",
            font=("Segoe UI", 9),
            fg="#d0d0d0",
            bg="#1d3557",
        )
        self.date_label.pack(anchor="e")

        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.now()

        self.time_label.config(
            text=now.strftime("%d-%m-%Y   %H:%M:%S")
        )

        self.date_label.config(
            text=now.strftime("%A")
        )

        self.after(1000, self.update_clock)