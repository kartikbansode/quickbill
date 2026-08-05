import tkinter as tk


class Toolbar(tk.Frame):

    def __init__(self, parent, callbacks):
        super().__init__(parent, bg="#f2f2f2", height=45)

        self.pack(fill="x")

        buttons = [

            ("🆕 New Bill", callbacks.get("new_bill")),
            ("💾 Save", callbacks.get("save_bill")),
            ("🖨 Print", callbacks.get("print_bill")),
            ("📋 Hold", callbacks.get("hold_bill")),
            ("🔍 Find Bill", callbacks.get("find_bill")),
            ("📦 Products", callbacks.get("products")),
            ("👤 Customers", callbacks.get("customers")),
            ("📊 Reports", callbacks.get("reports")),
            ("⚙ Settings", callbacks.get("settings")),
            ("❌ Exit", callbacks.get("exit"))

        ]

        for text, command in buttons:

            tk.Button(
                self,
                text=text,
                command=command,
                bg="white",
                fg="#222222",
                relief="ridge",
                bd=1,
                padx=10,
                pady=6,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2"
            ).pack(side="left", padx=2, pady=4)