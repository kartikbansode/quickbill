import tkinter as tk


class Toolbar(tk.Frame):

    def __init__(self, parent, callbacks):
        super().__init__(parent, bg="#e5e7eb", height=55)

        self.pack(fill="x")

        buttons = [

            ("Billing", callbacks.get("billing")),

            ("New Bill", callbacks.get("new_bill")),

            ("Save", callbacks.get("save_bill")),

            ("Print", callbacks.get("print_bill")),

            ("Hold", callbacks.get("hold_bill")),

            ("Find Bill", callbacks.get("find_bill")),

            ("Products", callbacks.get("products")),

            ("Customers", callbacks.get("customers")),

            ("Reports", callbacks.get("reports")),

            ("Settings", callbacks.get("settings")),

            ("Exit", callbacks.get("exit"))

        ]

        for text, command in buttons:

            btn = tk.Button(
                self,
                text=text,
                command=command,
                bg="#ffffff",
                fg="#1f2937",
                activebackground="#2563eb",
                activeforeground="white",
                relief="flat",
                bd=0,
                width=12,
                height=2,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            )

            btn.pack(side="left", padx=4, pady=5)

            btn.bind(
                "<Enter>",
                lambda e, b=btn: b.config(bg="#2563eb", fg="white")
            )

            btn.bind(
                "<Leave>",
                lambda e, b=btn: b.config(bg="#ffffff", fg="#1f2937")
            )