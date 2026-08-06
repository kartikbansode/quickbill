import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time

from logic.resource_path import resource_path


class SplashScreen:

    def __init__(self):

        self.root = tk.Tk()

        self.root.withdraw()

        self.root.overrideredirect(True)

        self.root.deiconify()

        self.root.configure(bg="white")

        self.root.resizable(False, False)

        self.build_ui()

        self.root.update_idletasks()

        content_width = self.card.winfo_reqwidth()
        content_height = self.card.winfo_reqheight()

        window_width = content_width + 2
        window_height = content_height + 2

        # Fixed professional splash size

        window_width = 650
        window_height = 450

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.attributes("-alpha", 0.0)

        self.fade_in()

    def fade_in(self):

        alpha = 0.0

        while alpha < 1:

            alpha += 0.05

            self.root.attributes("-alpha", alpha)

            self.root.update()

            time.sleep(0.015)

    def fade_out(self):

        alpha = 1

        while alpha > 0:

            alpha -= 0.05

            self.root.attributes("-alpha", alpha)

            self.root.update()

            time.sleep(0.015)

    # -------------------------------------------------

    def build_ui(self):

        # ===========================
        # Main Card
        # ===========================

        self.card = tk.Frame(
            self.root,
            bg="white",
        )

        self.card.pack(fill="both", expand=True)

        # Blue Accent

        tk.Frame(
            self.card,
            bg="#0057D8",
            height=6,
        ).pack(fill="x")

        # ===========================
        # Header
        # ===========================

        header = tk.Frame(
            self.card,
            bg="white",
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(28, 20),
        )

        try:

            image = Image.open(resource_path("assets/images/logo.png"))

            image.thumbnail((58, 58))

            self.logo = ImageTk.PhotoImage(image)

            tk.Label(
                header,
                image=self.logo,
                bg="white",
            ).pack(side="left")

        except:

            pass

        title_frame = tk.Frame(
            header,
            bg="white",
        )

        title_frame.pack(
            side="left",
            padx=18,
        )

        tk.Label(
            title_frame,
            text="QuickBill",
            bg="white",
            fg="#1E293B",
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Professional POS Billing Software",
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 11),
        ).pack(anchor="w")

        tk.Frame(
            self.card,
            bg="#E2E8F0",
            height=2,
        ).pack(fill="x", pady=(10, 0))

        # ==========================
        # Loading Status
        # ==========================

        body = tk.Frame(
            self.card,
            bg="white",
        )

        body.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(15, 10),
        )

        self.loading_title = tk.StringVar(value="Initializing Modules...")

        tk.Label(
            body,
            textvariable=self.loading_title,
            bg="white",
            fg="#1E293B",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")

        self.step_labels = []

        steps = [
            "Loading Product Database",
            "Loading Billing Database",
            "Loading Inventory",
            "Preparing Workspace",
            "Starting Barcode Scanner",
        ]

        for step in steps:

            lbl = tk.Label(
                body,
                text="○  " + step,
                bg="white",
                fg="#64748B",
                font=("Segoe UI", 10),
            )

            lbl.pack(
                anchor="w",
                pady=2,
            )

            self.step_labels.append(lbl)

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "QB.Horizontal.TProgressbar",
            thickness=8,
            troughcolor="#E2E8F0",
            background="#2563EB",
            borderwidth=0,
        )

        self.progress = ttk.Progressbar(
            body,
            style="QB.Horizontal.TProgressbar",
            mode="determinate",
            length=560,
            maximum=100,
        )

        self.progress.pack(
            pady=(25, 8),
            fill="x",
        )

        self.status = tk.StringVar(value="Starting...")

        tk.Label(
            body,
            textvariable=self.status,
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        # ---------------- Footer ----------------

        footer = tk.Frame(
            body,
            bg="white",
        )

        footer.pack(
            fill="x",
            pady=(8, 0),
        )

        tk.Frame(
            footer,
            bg="#E5E7EB",
            height=1,
        ).pack(fill="x", pady=(0, 10))

        bottom = tk.Frame(
            footer,
            bg="white",
        )

        bottom.pack(fill="x")

        tk.Label(
            bottom,
            text="Professional Edition",
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 9),
        ).pack(side="left")

        tk.Label(
            bottom,
            text="Build 1.0.0",
            bg="white",
            fg="#64748B",
            font=("Segoe UI", 9),
        ).pack(side="right")

    # -------------------------------------------------

    def update_progress(self, value, message):

        current = self.progress["value"]

        while current < value:

            current += 1

            self.progress["value"] = current

            self.root.update()

            time.sleep(0.01)

        self.status.set(message)

        self.root.update()

        progress_steps = [
            20,
            40,
            60,
            80,
            100,
        ]

        for i, step in enumerate(progress_steps):

            if value >= step:

                self.step_labels[i].config(
                    text="✓  " + self.step_labels[i]["text"][3:],
                    fg="#16A34A",
                    font=("Segoe UI", 10, "bold"),
                )

            elif value >= step - 20:

                self.step_labels[i].config(
                    text="●  " + self.step_labels[i]["text"][3:],
                    fg="#2563EB",
                    font=("Segoe UI", 10, "bold"),
                )

    # -------------------------------------------------

    def close(self):

        self.fade_out()

        self.root.destroy()

    def update(self, value, message):
        self.update_progress(value, message)
