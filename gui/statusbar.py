import tkinter as tk


class StatusBar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#2d3436", height=28)

        self.pack_propagate(False)

        self.status = tk.StringVar(value="Ready")

        self.scanner = tk.StringVar(value="Disconnected")

        self.operator = tk.StringVar(value="Admin")

        self.version = tk.StringVar(value="v1.0")

        tk.Label(
            self,
            textvariable=self.status,
            bg="#2d3436",
            fg="white",
            font=("Segoe UI", 9)
        ).pack(side="left", padx=10)

        tk.Label(
            self,
            text="|",
            bg="#2d3436",
            fg="white"
        ).pack(side="left")

        tk.Label(
            self,
            text="Scanner:",
            bg="#2d3436",
            fg="white",
            font=("Segoe UI", 9)
        ).pack(side="left", padx=(10, 2))

        tk.Label(
            self,
            textvariable=self.scanner,
            bg="#2d3436",
            fg="#00e676",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        tk.Label(
            self,
            text="|",
            bg="#2d3436",
            fg="white"
        ).pack(side="left", padx=10)

        tk.Label(
            self,
            text="Operator:",
            bg="#2d3436",
            fg="white",
            font=("Segoe UI", 9)
        ).pack(side="left")

        tk.Label(
            self,
            textvariable=self.operator,
            bg="#2d3436",
            fg="white",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(5, 10))

        tk.Label(
            self,
            textvariable=self.version,
            bg="#2d3436",
            fg="#dfe6e9",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=10)

    def set_status(self, text):
        self.status.set(text)

    def scanner_connected(self):
        self.scanner.set("Connected")

    def scanner_disconnected(self):
        self.scanner.set("Disconnected")

    def set_operator(self, name):
        self.operator.set(name)