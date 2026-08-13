import tkinter as tk


class Toolbar(tk.Frame):

    def __init__(self, parent, callbacks):
        super().__init__(parent, bg="#e5e7eb")

        self.buttons_data = [
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

        self.inner_frame = tk.Frame(self, bg="#e5e7eb")
        self.inner_frame.pack(expand=True, pady=2)

        self.btn_widgets = []
        for text, command in self.buttons_data:
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
                width=12,
                height=2,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            )
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2563eb", fg="white"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#ffffff", fg="#1f2937"))
            self.btn_widgets.append(btn)

        self.bind("<Configure>", self._on_resize)
        self._last_width = 0

    def _on_resize(self, event):
        if event.width <= 10 or event.width == self._last_width:
            return
        self._last_width = event.width

        max_btns = len(self.btn_widgets)
        btn_width = 120  # Safe width estimate (width=12 + padding)
        cols = max(1, event.width // btn_width)
        cols = min(cols, max_btns)

        for idx, btn in enumerate(self.btn_widgets):
            r = idx // cols
            c = idx % cols
            btn.grid(row=r, column=c, padx=4, pady=4)