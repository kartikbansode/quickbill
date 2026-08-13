import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk

from logic.resource_path import resource_path


class SplashScreen:

    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 450

    MIN_DISPLAY_TIME = 1800

    BACKGROUND = "#102A43"
    BORDER = "#16324F"
    ACCENT = "#2F6FED"
    TEXT = "#FFFFFF"
    MUTED = "#AFC0D1"

    def __init__(self, parent):

        self.parent = parent

        # ---------------------------------------------------------
        # Create Toplevel instead of another Tk root
        # ---------------------------------------------------------

        self.root = tk.Toplevel(parent)

        self.root.withdraw()

        self.root.overrideredirect(True)

        self.root.configure(
            bg=self.BACKGROUND
        )

        self.root.resizable(
            False,
            False
        )

        # ---------------------------------------------------------
        # Center splash
        # ---------------------------------------------------------

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = max(
            0,
            (screen_width - self.WINDOW_WIDTH) // 2
        )

        y = max(
            0,
            (screen_height - self.WINDOW_HEIGHT) // 2
        )

        self.root.geometry(
            f"{self.WINDOW_WIDTH}x"
            f"{self.WINDOW_HEIGHT}+{x}+{y}"
        )

        # ---------------------------------------------------------
        # State
        # ---------------------------------------------------------

        self._progress_value = 0.0
        self._progress_target = 0.0

        self._progress_job = None
        self._close_job = None
        self._fade_job = None

        self._closed = False

        self.start_time = self._current_time()

        # ---------------------------------------------------------
        # Transparency
        # ---------------------------------------------------------

        self._supports_alpha = True

        try:
            self.root.attributes(
                "-alpha",
                0.0
            )
        except tk.TclError:
            self._supports_alpha = False

        # ---------------------------------------------------------
        # Build UI
        # ---------------------------------------------------------

        self.build_ui()

        # ---------------------------------------------------------
        # Show splash
        # ---------------------------------------------------------

        self.root.deiconify()

        self.root.lift()

        self.root.focus_force()

        # ---------------------------------------------------------
        # Fade in
        # ---------------------------------------------------------

        self.fade_in()

        # Make sure the splash is visible immediately.
        self.root.update_idletasks()
        self.root.update()

    # =============================================================
    # BUILD UI
    # =============================================================

    def build_ui(self):

        main_frame = tk.Frame(
            self.root,
            bg=self.BACKGROUND,
            highlightbackground=self.BORDER,
            highlightthickness=1,
            bd=0,
        )

        main_frame.pack(
            fill="both",
            expand=True,
        )

        # ---------------------------------------------------------
        # Center content
        # ---------------------------------------------------------

        center_frame = tk.Frame(
            main_frame,
            bg=self.BACKGROUND,
            bd=0,
            highlightthickness=0,
        )

        center_frame.place(
            relx=0.5,
            rely=0.45,
            anchor="center",
        )

        # ---------------------------------------------------------
        # Logo
        # ---------------------------------------------------------

        self.logo = None

        try:

            image = Image.open(
                resource_path(
                    "assets/images/logo.png"
                )
            )

            image.thumbnail(
                (72, 72),
                Image.Resampling.LANCZOS
            )

            self.logo = ImageTk.PhotoImage(
                image
            )

            tk.Label(
                center_frame,
                image=self.logo,
                bg=self.BACKGROUND,
                bd=0,
                highlightthickness=0,
            ).pack(
                pady=(0, 14)
            )

        except Exception:
            pass

        # ---------------------------------------------------------
        # Brand
        # ---------------------------------------------------------

        tk.Label(
            center_frame,
            text="QUICKBILL PRO",
            bg=self.BACKGROUND,
            fg=self.TEXT,
            font=("Segoe UI", 30, "bold"),
            bd=0,
            highlightthickness=0,
        ).pack()

        tk.Label(
            center_frame,
            text="Professional Billing & POS",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 12),
            bd=0,
            highlightthickness=0,
        ).pack(
            pady=(5, 34)
        )

        # ---------------------------------------------------------
        # Status
        # ---------------------------------------------------------

        self.status = tk.StringVar(
            value="Starting QuickBill..."
        )

        tk.Label(
            center_frame,
            textvariable=self.status,
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=0,
        ).pack(
            pady=(0, 9)
        )

        # ---------------------------------------------------------
        # Progress bar
        # ---------------------------------------------------------

        style = ttk.Style(
            self.root
        )

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "QuickBill.Splash.Horizontal.TProgressbar",
            thickness=4,
            troughcolor="#16324F",
            background=self.ACCENT,
            bordercolor=self.BACKGROUND,
            lightcolor=self.ACCENT,
            darkcolor=self.ACCENT,
        )

        self.progress = ttk.Progressbar(
            center_frame,
            style="QuickBill.Splash.Horizontal.TProgressbar",
            mode="determinate",
            length=400,
            maximum=100,
        )

        self.progress.pack()

        # ---------------------------------------------------------
        # Footer
        # ---------------------------------------------------------

        footer = tk.Frame(
            main_frame,
            bg=self.BACKGROUND,
            bd=0,
            highlightthickness=0,
        )

        footer.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=15,
        )

        tk.Label(
            footer,
            text="Version 1.0.0",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 9),
            bd=0,
        ).pack(
            side="left"
        )

        tk.Label(
            footer,
            text="© 2026 QuickBill",
            bg=self.BACKGROUND,
            fg=self.MUTED,
            font=("Segoe UI", 9),
            bd=0,
        ).pack(
            side="right"
        )

    # =============================================================
    # UPDATE
    # =============================================================

    def update(self, value, message):

        if self._closed:
            return

        try:
            value = float(value)
        except (TypeError, ValueError):
            return

        value = max(0.0, min(100.0, value))

        if value < self._progress_value:
            value = self._progress_value

        self._progress_target = value

        self.status.set(str(message))

        import time
        while self._progress_value < self._progress_target and not self._closed:
            difference = self._progress_target - self._progress_value
            step = max(0.35, min(2.5, difference * 0.14))
            
            self._progress_value += step
            
            if self._progress_value > self._progress_target:
                self._progress_value = self._progress_target
                
            self.progress["value"] = self._progress_value
            self._process_events()
            time.sleep(0.015)

    # =============================================================
    # PROCESS EVENTS
    # =============================================================

    def _process_events(self):

        try:
            self.root.update_idletasks()
            self.root.update()

        except tk.TclError:
            pass

    # =============================================================
    # FADE IN
    # =============================================================

    def fade_in(self):

        if self._closed:
            return

        if not self._supports_alpha:
            return

        try:

            alpha = float(
                self.root.attributes("-alpha")
            )

            if alpha >= 1.0:

                self.root.attributes(
                    "-alpha",
                    1.0
                )

                self._fade_job = None

                return

            alpha += 0.08

            alpha = min(
                alpha,
                1.0
            )

            self.root.attributes(
                "-alpha",
                alpha
            )

            self._fade_job = self.root.after(
                20,
                self.fade_in
            )

        except tk.TclError:

            self._fade_job = None

    # =============================================================
    # CLOSE
    # =============================================================

    def close(self):

        if self._closed:
            return

        # Final state
        self._progress_target = 100

        self.status.set(
            "Launching QuickBill..."
        )

        self._wait_until_ready_to_close()

    # =============================================================
    # WAIT FOR FINAL CLOSE
    # =============================================================

    def _wait_until_ready_to_close(self):

        import time
        while not self._closed:
            elapsed = (
                self._current_time()
                - self.start_time
            )

            minimum_time_reached = (
                elapsed * 1000
                >= self.MIN_DISPLAY_TIME
            )

            progress_finished = (
                self._progress_value >= 99.9
            )

            if (
                minimum_time_reached
                and progress_finished
            ):
                self._destroy_splash()
                return

            self._process_events()
            time.sleep(0.015)

    # =============================================================
    # DESTROY SPLASH
    # =============================================================

    def _destroy_splash(self):

        if self._closed:
            return

        self._closed = True

        # Cancel animations
        for job in (
            self._progress_job,
            self._close_job,
            self._fade_job,
        ):

            if job is not None:

                try:
                    self.root.after_cancel(job)
                except tk.TclError:
                    pass

        self._progress_job = None
        self._close_job = None
        self._fade_job = None

        try:
            self.root.attributes(
                "-alpha",
                0.0
            )
        except tk.TclError:
            pass

        try:
            self.root.withdraw()
        except tk.TclError:
            pass

        try:
            self.root.destroy()
        except tk.TclError:
            pass

        # Critical:
        # make sure the parent root processes the destruction
        # before the main application is shown.
        try:
            self.parent.update_idletasks()
            self.parent.update()
        except tk.TclError:
            pass

    # =============================================================
    # TIME
    # =============================================================

    def _current_time(self):

        return (
            self.root.tk.call(
                "clock",
                "milliseconds"
            ) / 1000.0
        )

    # =============================================================
    # COMPATIBILITY
    # =============================================================

    def update_idletasks(self):

        try:
            self.root.update_idletasks()
        except tk.TclError:
            pass