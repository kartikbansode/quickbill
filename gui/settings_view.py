import tkinter as tk
from tkinter import messagebox
from gui.ui_components import create_success_button, FONT_LABEL, FONT_SECTION


class SettingsView(tk.Frame):
    def __init__(self, parent, webcam_url="", save_callback=None):
        super().__init__(parent, bg="#f4f6f9")

        self.save_callback = save_callback

        title = tk.Label(
            self,
            text="Settings",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f6f9",
            fg="#1f2937",
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))

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

        save_btn = create_success_button(
            scanner_frame,
            text="Save",
            command=self.save_settings,
        )

        save_btn.grid(row=1, column=1)

        scanner_frame.columnconfigure(0, weight=1)

    def save_settings(self):

        if self.save_callback:

            self.save_callback(self.url_var.get().strip())

            messagebox.showinfo(
                "Settings",
                "Webcam URL saved successfully."
            )

    def get_webcam_url(self):
        return self.url_var.get().strip()

    def set_webcam_url(self, url):
        self.url_var.set(url)