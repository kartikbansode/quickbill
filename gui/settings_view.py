import tkinter as tk
from tkinter import messagebox
from gui.ui_components import create_success_button, FONT_LABEL, FONT_SECTION


class SettingsView(tk.Frame):
    def __init__(self, parent, webcam_url="", upi_id="", save_callback=None, save_payment_callback=None):
        super().__init__(parent, bg="#f4f6f9")

        self.save_callback = save_callback
        self.save_payment_callback = save_payment_callback

        title = tk.Label(
            self,
            text="Settings",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f6f9",
            fg="#1f2937",
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))

        # --- Scanner Settings ---
        scanner_frame = tk.LabelFrame(
            self,
            text="Scanner Settings",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            padx=15,
            pady=15,
        )

        scanner_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            scanner_frame,
            text="Webcam URL",
            font=("Segoe UI", 10),
            bg="white",
        ).grid(row=0, column=0, sticky="w")

        self.url_var = tk.StringVar(value=webcam_url)

        self.url_entry = tk.Entry(
            scanner_frame,
            textvariable=self.url_var,
            font=("Segoe UI", 10),
            width=60,
        )

        self.url_entry.grid(
            row=1,
            column=0,
            padx=(0, 10),
            pady=10,
            sticky="ew",
        )

        save_scanner_btn = create_success_button(
            scanner_frame,
            text="Save",
            command=self.save_scanner_settings,
        )

        save_scanner_btn.grid(row=1, column=1)

        scanner_frame.columnconfigure(0, weight=1)

        # --- Payment Settings ---
        payment_frame = tk.LabelFrame(
            self,
            text="Payment Settings",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            padx=15,
            pady=15,
        )

        payment_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            payment_frame,
            text="UPI ID",
            font=("Segoe UI", 10, "bold"),
            bg="white",
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            payment_frame,
            text="UPI ID used to generate customer payment QR codes.",
            font=("Segoe UI", 9),
            fg="#6b7280",
            bg="white",
        ).grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.upi_var = tk.StringVar(value=upi_id)

        self.upi_entry = tk.Entry(
            payment_frame,
            textvariable=self.upi_var,
            font=("Segoe UI", 10),
            width=60,
        )

        self.upi_entry.grid(
            row=2,
            column=0,
            padx=(0, 10),
            pady=(0, 10),
            sticky="ew",
        )

        save_payment_btn = create_success_button(
            payment_frame,
            text="Save",
            command=self.save_payment_settings,
        )

        save_payment_btn.grid(row=2, column=1, pady=(0, 10))

        payment_frame.columnconfigure(0, weight=1)

    def save_scanner_settings(self):
        if self.save_callback:
            self.save_callback(self.url_var.get().strip())
            messagebox.showinfo("Settings", "Webcam URL saved successfully.")

    def save_payment_settings(self):
        upi_id = self.upi_var.get().strip()
        if self.save_payment_callback:
            self.save_payment_callback(upi_id)
            messagebox.showinfo("Settings", "UPI ID saved successfully.")