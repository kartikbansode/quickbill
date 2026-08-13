import tkinter as tk


class Toolbar(tk.Frame):

    def __init__(self, parent, callbacks):
        super().__init__(parent, bg="#e5e7eb")

        self.buttons_data = [
            ("Billing", callbacks.get("billing")),
            ("New Bill", callbacks.get("new_bill")),
            #("Save", callbacks.get("save_bill")),
            #("Print", callbacks.get("print_bill")),
            ("Hold", callbacks.get("hold_bill")),
            ("Find Bill", callbacks.get("find_bill")),
            ("Products", callbacks.get("products")),
            #("Customers", callbacks.get("customers")),
            #("Reports", callbacks.get("reports")),
            ("Settings", callbacks.get("settings")),
            ("Exit", callbacks.get("exit"))
        ]

        self.inner_frame = tk.Frame(self, bg="#e5e7eb")
        self.inner_frame.pack(fill="x", expand=True, pady=2, padx=2)

        for c in range(len(self.buttons_data)):
            self.inner_frame.columnconfigure(c, weight=1)

        self.btn_widgets = []
        for idx, (text, command) in enumerate(self.buttons_data):
            btn = tk.Button(
                self.inner_frame,
                text=text,
                command=command,
                bg="#ffffff",
                fg="#1f2937",
                activebackground="#2563eb",
                activeforeground="white",
                relief="flat",
                bd=0,
                height=2,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            )
            btn.grid(row=0, column=idx, sticky="ew", padx=2, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2563eb", fg="white"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ffffff", fg="#1f2937"))
            self.btn_widgets.append(btn)