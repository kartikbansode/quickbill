import tkinter as tk
from tkinter import messagebox

from gui.splash_screen import SplashScreen
from gui.main_window import launch_main_window

from logic.database import (
    init_product_db,
    init_bill_db,
)

from logic.customer_display_server import customer_display


APP_NAME = "QuickBill Pro"


def main():
    """
    QuickBill application entry point.

    A single Tk root is created here.
    The splash screen is a Toplevel belonging to that root.
    The main application is launched only after the splash
    has been completely destroyed.
    """

    root = tk.Tk()

    # Keep the root hidden while the splash is displayed.
    root.withdraw()

    splash = SplashScreen(root)

    try:
        # ---------------------------------------------------------
        # Initializing application
        # ---------------------------------------------------------

        splash.update(
            10,
            "Initializing QuickBill..."
        )

        root.update_idletasks()
        root.update()

        # ---------------------------------------------------------
        # Product database
        # ---------------------------------------------------------

        splash.update(
            30,
            "Loading Product Database..."
        )

        root.update_idletasks()
        root.update()

        init_product_db()

        # ---------------------------------------------------------
        # Billing database
        # ---------------------------------------------------------

        splash.update(
            55,
            "Loading Billing History..."
        )

        root.update_idletasks()
        root.update()

        init_bill_db()

        # ---------------------------------------------------------
        # Workspace
        # ---------------------------------------------------------

        splash.update(
            70,
            "Preparing Workspace..."
        )

        root.update_idletasks()
        root.update()

        # ---------------------------------------------------------
        # Barcode scanner
        # ---------------------------------------------------------

        splash.update(
            82,
            "Initializing Barcode Scanner..."
        )

        root.update_idletasks()
        root.update()

        # Scanner initialization is handled by the
        # billing/scanner modules when the main window starts.

        # ---------------------------------------------------------
        # Customer display
        # ---------------------------------------------------------

        splash.update(
            92,
            "Starting Customer Display..."
        )

        root.update_idletasks()
        root.update()

        customer_display.start()

        # ---------------------------------------------------------
        # Final startup state
        # ---------------------------------------------------------

        splash.update(
            100,
            "Launching QuickBill..."
        )

        root.update_idletasks()
        root.update()

        # ---------------------------------------------------------
        # IMPORTANT
        #
        # SplashScreen.close() is now synchronous.
        # It does not return until the splash has actually
        # been destroyed.
        # ---------------------------------------------------------

        splash.close()

        # ---------------------------------------------------------
        # Show the main application ONLY after the splash
        # has completely disappeared and the UI is built.
        # ---------------------------------------------------------

        launch_main_window(root)

    except Exception as exc:

        _handle_startup_error(
            root,
            splash,
            exc,
        )


def _handle_startup_error(root, splash, error):
    """
    Cleanly handle startup failures.
    """

    try:
        splash.close()
    except Exception:
        pass

    try:
        root.deiconify()
        root.withdraw()
    except Exception:
        pass

    message = (
        f"{APP_NAME} could not start.\n\n"
        "An error occurred while initializing "
        "the application.\n\n"
        f"Error: {error}"
    )

    try:
        messagebox.showerror(
            APP_NAME,
            message,
            parent=root,
        )
    finally:
        try:
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    main()