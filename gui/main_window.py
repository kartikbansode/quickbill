import tkinter as tk
from tkinter import ttk, messagebox
from logic.cart import cart, add_to_cart, remove_from_cart, update_quantity
from logic.billing import calculate_totals
from logic.barcode_scanner import scan_barcode_background, stop_scanner, play_beep, get_scanner_status
from logic.database import (
    get_product_by_barcode,
    add_product,
    edit_product,
    delete_product,
    get_all_products,
    search_products,
)
import os
import json
from gui.toolbar import Toolbar
from gui.header import Header
from gui.statusbar import StatusBar
from gui.billing.billing_view import BillingView
from gui.product_master import ProductMaster
from gui.settings_view import SettingsView
from gui.payment.payment_dialog import PaymentDialog
from logic.hold_bill import hold_bill
from gui.hold_bill.hold_bill_window import HoldBillWindow
from gui.find_bill.find_bill_view import FindBillView
from logic.bill_history import (
    get_all_bills,
    search_bill_history,
)
from logic.database import generate_bill_number
from gui.find_bill.bill_details_dialog import BillDetailsDialog
from logic.file_paths import data_path
from logic.customer_display_server import customer_display
from logic.pdf_generator import generate_pdf_bill
from logic.resource_path import resource_path
from logic.app_state import app_state
from logic.config import get, set

scanner_active = False

try:
    webcam_url = get("scanner", "camera_url")
except Exception:
    webcam_url = "http://192.168.0.203:8080/video"


BILLS_HISTORY_FILE = data_path("bills_history.json")


def launch_main_window():

    window = tk.Tk()

    def close_application():
        try:
            customer_display.stop()
        except Exception:
            pass

        try:
            window.destroy()
        except Exception:
            pass

    window.protocol(
        "WM_DELETE_WINDOW",
        close_application,
    )

    window.attributes("-fullscreen", True)

    window.title("QuickBill System")

    window.bind(
        "<Escape>",
        lambda e: window.attributes("-fullscreen", False),
    )

    find_bill_view = None
    settings_view = None
    product_view = None
    billing_view = None

    # Payment dialog lifecycle guard.
    # Only one payment transaction may exist at a time.
    payment_dialog = None
    payment_in_progress = False
    try:
        logo = tk.PhotoImage(file=resource_path("assets/images/logo.png"))
        window.iconphoto(True, logo)
    except Exception as e:
        print("Unable to load icon:", e)

    # Set window size and center it
    window_width = 1000
    window_height = 650
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.configure(bg="#e9ecef")
    window.resizable(True, True)  # Enable resizing and maximize button

    # Custom style for professional look
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TButton",
        font=("Helvetica", 10, "bold"),
        padding=8,
        background="#007bff",
        foreground="white",
    )
    style.map("TButton", background=[("active", "#0056b3")])
    style.configure(
        "TLabelFrame",
        font=("Helvetica", 11, "bold"),
        foreground="#2c3e50",
        background="white",
    )
    style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
    style.configure(
        "Treeview.Heading",
        font=("Helvetica", 10, "bold"),
        background="#007bff",
        foreground="white",
    )
    style.configure("Bold.Treeview", font=("Helvetica", 9, "bold"))

    # --- Menu Bar ---
    header = Header(window)
    header.pack(side="top", fill="x")

    status_bar = StatusBar(window)
    status_bar.pack(side="bottom", fill="x")

    # --- Content Container ---
    content_container = tk.Frame(window, bg="#e9ecef")
    # Will pack this at the bottom of the file after everything else is created,
    # or just let it expand in the middle.
    content_container.pack(side="top", fill=tk.BOTH, expand=True, padx=5, pady=5)

    def broadcast_current_bill():
        """
        Send the complete current billing state to the optional
        Android customer display.

        The Android display is never required for billing.
        Any failure here must not affect QuickBill.
        """

        try:

            subtotal, tax, discount, total = calculate_totals()

            items = []

            for item in cart:

                rate = float(
                    item.get(
                        "selling_price",
                        item.get("price", 0),
                    )
                )

                qty = int(item.get("qty", 0))

                items.append(
                    {
                        "barcode": item.get("barcode", ""),
                        "sku": item.get("sku", ""),
                        "name": item.get("name", ""),
                        "brand": item.get("brand", ""),
                        "category": item.get("category", ""),
                        "qty": qty,
                        "rate": rate,
                        "amount": round(rate * qty, 2),
                        "gst": item.get("gst", 0),
                    }
                )

            message = {
                "type": "bill_update",
                "bill_no": bill_number,
                "customer": {
                    "name": "Walk-in Customer",
                    "mobile": "",
                },
                "items": items,
                "subtotal": round(subtotal, 2),
                "tax": round(tax, 2),
                "discount": round(discount, 2),
                "total": round(total, 2),
                "payment": {
                    "status": "pending",
                    "mode": None,
                },
            }

            customer_display.broadcast(message)

        except Exception as exc:

            # Customer display is optional.
            # Never allow it to affect billing.
            print(f"[CustomerDisplay] Bill broadcast skipped: {exc}")

    def refresh_table():
        if billing_view is None:
            return

        billing_view.render_cart(cart)
        billing_view.refresh_totals()

        # --------------------------------
        # Customer Display
        # --------------------------------
        try:
            subtotal, tax, discount, total = calculate_totals()

            customer_display.bill_update(
                bill_no=bill_number,
                items=cart,
                subtotal=subtotal,
                tax=tax,
                discount=discount,
                total=total,
                customer=app_state.current_customer,
                cashier=app_state.operator,
            )

        except Exception as exc:
            # Customer display is optional.
            # Never allow it to affect desktop billing.
            print("[CustomerDisplay] " f"Bill update failed: {exc}")

    def update_totals():
        if billing_view is not None:
            billing_view.refresh_totals()

    def add_manual_barcode():
        if billing_view is None:
            return

        barcode = billing_view.get_manual_barcode()

        if barcode:

            on_barcode_detected(barcode)

            billing_view.clear_manual_barcode()

            billing_view.focus_manual_barcode()

    def clear_cart_all():
        if messagebox.askyesno(
            "Clear All", "Are you sure you want to clear the entire cart?"
        ):
            cart.clear()
            refresh_table()

    def update_item_qty(index, delta):
        current = cart[index]["qty"]
        new_qty = current + delta
        if new_qty < 1:
            remove_from_cart(index)
        else:
            update_quantity(index, new_qty)
        refresh_table()

    def increase_item_qty(index):
        update_item_qty(index, 1)

    def decrease_item_qty(index):
        update_item_qty(index, -1)

    def delete_item(index):
        remove_from_cart(index)
        refresh_table()

    def start_scan():
        scanner_ok, scanner_err = get_scanner_status()
        if not scanner_ok:
            messagebox.showwarning(
                "Scanner Unavailable",
                scanner_err,
                parent=window,
            )
            return

        global scanner_active

        # Scanner is already running.
        if scanner_active:
            return

        scanner_active = True

        billing_view.update_scanner_status("Scanner Active")

        status_bar.scanner_connected()
        status_bar.set_status("Scanning Product")

        scan_barcode_background(
            webcam_url,
            on_barcode_detected,
        )

        billing_view.scanner_panel.scan_button.config(
            text="Stop Scanner",
            command=stop_scan,
        )

    def stop_scan():

        global scanner_active

        if not scanner_active:
            return

        stop_scanner()

        scanner_active = False

        billing_view.update_scanner_status("Scanner Stopped")

        status_bar.scanner_disconnected()

        status_bar.set_status("Scanner Stopped")

        billing_view.scanner_panel.scan_button.config(
            text="Start Scanner",
            command=start_scan,
        )

    # =====================================================
    # Customer Display - Payment Events
    # =====================================================

    def customer_display_payment_started(
        mode,
        total,
        qr=None,
    ):
        """
        Synchronize the current payment state with the
        optional Android Customer Display.

        Desktop remains the source of truth.
        Android only displays the received state.
        """

        try:

            mode = str(mode).strip()

            customer_display.payment_started(
                bill_number,
                mode,
                float(total),
                qr=qr,
            )

            if mode.upper() == "UPI":

                customer_display.payment_pending(
                    bill_number,
                    mode,
                    float(total),
                    qr=qr,
                )

        except Exception as exc:

            print("[CustomerDisplay] " f"Payment start notification failed: {exc}")

    def customer_display_payment_cancelled(mode):
        """
        Notify Android that the payment dialog was
        cancelled and return the customer display
        to the billing screen.
        """

        nonlocal payment_dialog
        nonlocal payment_in_progress

        try:

            customer_display.payment_cancelled(
                bill_number,
                mode,
            )

        except Exception as exc:

            print("[CustomerDisplay] " f"Payment cancel notification failed: {exc}")

        payment_dialog = None
        payment_in_progress = False

        show_billing_view()

        try:

            window.after(
                80,
                billing_view.focus_manual_barcode,
            )

        except Exception:
            pass

    def open_payment_dialog():

        nonlocal payment_dialog
        nonlocal payment_in_progress

        if payment_in_progress:

            if payment_dialog is not None:

                try:

                    if payment_dialog.winfo_exists():

                        payment_dialog.lift()
                        payment_dialog.focus_force()

                        return

                except tk.TclError:
                    pass

            payment_dialog = None
            payment_in_progress = False

        if not cart:

            messagebox.showwarning(
                "Empty Bill",
                "Please add at least one product.",
                parent=window,
            )

            return

        _subtotal, _tax, _discount, total = calculate_totals()

        payment_in_progress = True

        try:

            dialog = PaymentDialog(
                window,
                total,
                complete_sale,
                on_payment_start=customer_display_payment_started,
                on_payment_cancel=customer_display_payment_cancelled,
                bill_no=bill_number,
            )

            payment_dialog = dialog

            def on_dialog_destroy(event):

                nonlocal payment_dialog
                nonlocal payment_in_progress

                if event.widget is dialog:

                    payment_dialog = None

                    if not dialog._processing:
                        payment_in_progress = False

            dialog.bind(
                "<Destroy>",
                on_dialog_destroy,
                add="+",
            )

        except Exception:

            payment_dialog = None
            payment_in_progress = False

            raise

    def complete_sale(payment_mode, received_amount):
        if getattr(window, "is_completing_sale", False):
            return

        window.is_completing_sale = True

        nonlocal bill_number, payment_dialog, payment_in_progress

        completed_bill = bill_number

        try:

            # --------------------------------
            # Calculate final total
            # --------------------------------

            subtotal, tax, discount, total = calculate_totals()

            # --------------------------------
            # Generate A4 + 80mm PDFs
            # --------------------------------

            generate_pdf_bill(
                cart,
                completed_bill,
                payment_mode,
                received_amount,
            )

            # --------------------------------
            # Reduce Product Stock
            # --------------------------------

            for item in cart:

                product = get_product_by_barcode(item["barcode"])

                if product:

                    current_stock = int(product.get("stock", 0))

                    product["stock"] = max(
                        0,
                        current_stock - int(item["qty"]),
                    )

                    edit_product(
                        product["barcode"],
                        product,
                    )

            # --------------------------------
            # Refresh Product Table
            # --------------------------------

            product_view.refresh_table()

            # --------------------------------
            # Clear Current Cart
            # --------------------------------

            cart.clear()

            billing_view.render_cart(cart)
            billing_view.refresh_totals()

            # --------------------------------
            # Customer Display
            # Payment Completed
            # --------------------------------

            try:

                customer_display.payment_completed(
                    completed_bill,
                    payment_mode,
                    total,
                )

                customer_display.sale_completed(
                    completed_bill,
                    payment_mode,
                    total,
                )

            except Exception as exc:

                print("[CustomerDisplay] " f"Completion notification failed: {exc}")

            # --------------------------------
            # Generate Next Bill Number
            # --------------------------------

            bill_number = generate_bill_number()

            billing_view.set_bill_number(bill_number)
            status_bar.set_bill_number(bill_number)

            # --------------------------------
            # Customer Display - New Bill
            # --------------------------------

            try:

                customer_display.new_bill(
                    bill_number,
                    customer=app_state.current_customer,
                    cashier=app_state.operator,
                )

            except Exception as exc:

                print("[CustomerDisplay] " f"New bill notification failed: {exc}")

            # --------------------------------
            # Always return to billing
            # --------------------------------

            show_billing_view()

            payment_in_progress = False
            payment_dialog = None

            try:
                window.after(
                    80,
                    billing_view.focus_manual_barcode,
                )
            except Exception:
                pass

            # --------------------------------
            # Success Message
            # --------------------------------

            status_bar.set_status(f"Bill {completed_bill} Generated Successfully.", timeout=5000)

            return True

        except Exception as e:

            # --------------------------------
            # Sale Error
            # --------------------------------

            payment_in_progress = False

            messagebox.showerror(
                "Sale Error",
                f"Unable to complete the sale.\n\n{e}",
                parent=window,
            )

            # Keep the payment dialog open so the cashier can retry.
            return False
            
        finally:
            window.is_completing_sale = False

    def search_bill(keyword):

        find_bill_view.clear_table()

        bills = search_bill_history(keyword)

        bills.reverse()

        if not bills:
            if keyword:
                find_bill_view.bill_tree.insert("", tk.END, values=("", f"No bills found for '{keyword}'", "", "", ""), tags=("empty",))
            else:
                find_bill_view.bill_tree.insert("", tk.END, values=("", "No bills found.", "", "", ""), tags=("empty",))
            return

        for bill in bills:

            find_bill_view.add_bill(
                bill["bill_no"],
                bill["date"],
                bill.get("payment_mode", "-"),
                len(bill["items"]),
                f"₹ {bill['total']:.2f}",
            )

    def open_bill_details(bill_no):

        bills = get_all_bills()

        for bill in bills:

            if bill["bill_no"] == bill_no:

                BillDetailsDialog(
                    window,
                    bill,
                )

                return

        messagebox.showerror(
            "Bill Not Found",
            f"Invoice {bill_no} was not found.",
        )

    def reprint_bill(bill_no):

        bills = get_all_bills()

        for bill in bills:

            if bill["bill_no"] != bill_no:
                continue

            try:

                # --------------------------------
                # Rebuild A4 + 80mm PDFs
                # WITHOUT creating another
                # bill-history entry.
                # --------------------------------

                result = generate_pdf_bill(
                    bill["items"],
                    bill["bill_no"],
                    bill.get(
                        "payment_mode",
                        "Cash",
                    ),
                    bill.get(
                        "received_amount",
                        bill.get(
                            "total",
                            0,
                        ),
                    ),
                    cashier=bill.get(
                        "cashier",
                        "Admin",
                    ),
                    save_history=False,
                )

                # --------------------------------
                # Show success
                # --------------------------------

                messagebox.showinfo(
                    "Reprint Successful",
                    (
                        f"Invoice {bill_no} regenerated successfully.\n\n"
                        "A4 and 80mm PDFs are ready."
                    ),
                )

                return

            except Exception as e:

                messagebox.showerror(
                    "Reprint Error",
                    f"Unable to regenerate invoice.\n\n{e}",
                )

                return

        messagebox.showerror(
            "Bill Not Found",
            f"Invoice {bill_no} was not found.",
        )

    def delete_bill(bill_no):

        if not messagebox.askyesno(
            "Delete Bill", f"Are you sure you want to delete\n{bill_no}?"
        ):
            return

        try:

            with open(BILLS_HISTORY_FILE, "r", encoding="utf-8") as file:
                bills = json.load(file)

            new_bills = [bill for bill in bills if bill["bill_no"] != bill_no]

            with open(BILLS_HISTORY_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    new_bills,
                    file,
                    indent=4,
                )

            load_bill_history()

            messagebox.showinfo("Success", "Bill deleted successfully.")

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
            )

    def on_barcode_detected(barcode):

        product = get_product_by_barcode(barcode)

        if product:

            add_to_cart(product)

            refresh_table()

            billing_view.display_product(product)

            billing_view.update_scanner_status("Product Added")

            status_bar.scanner_connected()

            status_bar.set_status(f"Added : {product['name']}")

        else:

            billing_view.update_scanner_status("Barcode Not Found")

            status_bar.set_status("Barcode Not Found")

    def hold_current_bill():

        nonlocal bill_number

        # -----------------------------------
        # Resume Existing Hold
        # -----------------------------------

        if not cart:

            HoldBillWindow(
                window,
                resume_hold_bill,
            )

            return

        # -----------------------------------
        # Hold Current Cart
        # -----------------------------------

        hold_no = hold_bill(cart.copy())

        messagebox.showinfo("Hold Bill", f"Current bill saved.\n\n{hold_no}")

        cart.clear()

        refresh_table()

    def resume_hold_bill(bill):

        nonlocal bill_number

        cart.clear()

        cart.extend(bill["cart"])

        refresh_table()

        bill_number = generate_bill_number()

        billing_view.set_bill_number(bill_number)

        status_bar.set_bill_number(bill_number)

        try:

            customer_display.bill_update(
                bill_no=bill_number,
                items=cart,
                subtotal=calculate_totals()[0],
                tax=calculate_totals()[1],
                discount=calculate_totals()[2],
                total=calculate_totals()[3],
                customer=app_state.current_customer,
                cashier=app_state.operator,
            )

        except Exception as exc:

            print("[CustomerDisplay] " f"Hold bill display update failed: {exc}")

        messagebox.showinfo("Hold Bill", f"{bill['hold_no']} resumed successfully.")

    billing_view = BillingView(
        content_container,
        {
            "generate_bill": open_payment_dialog,
            "clear_cart": clear_cart_all,
            "hold_bill": lambda: None,
            "start_scan": start_scan,
            "stop_scan": stop_scan,
            "barcode": on_barcode_detected,
            "increase_qty": increase_item_qty,
            "decrease_qty": decrease_item_qty,
            "delete_item": delete_item,
            "calculate_totals": calculate_totals,
        },
    )

    bill_number = generate_bill_number()
    status_bar.set_bill_number(bill_number)

    billing_view.set_bill_number(bill_number)

    billing_view.pack(fill="both", expand=True)

    # =====================================================
    # Product Master
    # =====================================================

    product_view = ProductMaster(content_container)

    # =====================================================
    # Settings
    # =====================================================

    def save_webcam_url(url):

        global webcam_url
        global scanner_active

        url = url.strip()

        if not url:

            messagebox.showwarning(
                "Invalid Scanner URL",
                "Please enter a valid camera stream URL.",
            )

            return

        webcam_url = url

        try:

            set(
                "scanner",
                "camera_url",
                webcam_url,
            )

            set(
                "scanner",
                "type",
                "mobile_camera",
            )

        except Exception as exc:

            messagebox.showerror(
                "Settings Error",
                f"Unable to save scanner settings.\n\n{exc}",
            )

            return

        # Restart is intentionally NOT automatic.
        #
        # If the scanner is currently running, stop it because
        # the old camera URL is no longer valid.
        if scanner_active:

            stop_scanner()

            scanner_active = False

            billing_view.update_scanner_status("Scanner Stopped")

            status_bar.scanner_disconnected()

        messagebox.showinfo(
            "Scanner Settings",
            "Scanner settings saved successfully.\n\n"
            "Press Start Scanner to connect using the new camera.",
        )

    # =====================================================
    # Settings View
    # =====================================================

    settings_view = SettingsView(
        content_container,
        webcam_url=webcam_url,
        save_callback=save_webcam_url,
    )

    # =====================================================
    # Find Bill Functions
    # =====================================================

    def start_bill_scan():

        global scanner_active

        if not scanner_active:

            scanner_active = True

            status_bar.scanner_connected()

            status_bar.set_status("Scanning Bill")

            scan_barcode_background(
                webcam_url,
                on_bill_barcode_detected,
            )

    def stop_bill_scan():

        global scanner_active

        if scanner_active:

            stop_scanner()

            scanner_active = False

            status_bar.scanner_disconnected()

            status_bar.set_status("Ready")

    def on_bill_barcode_detected(barcode):

        global scanner_active

        find_bill_view.bill_search_var.set(barcode)

        search_bill(barcode)

        stop_bill_scan()

    def load_bill_history():

        find_bill_view.clear_table()

        bills = get_all_bills()

        bills.reverse()

        for bill in bills:

            find_bill_view.add_bill(
                bill["bill_no"],
                bill["date"],
                bill.get("payment_mode", "-"),
                len(bill["items"]),
                f"₹ {bill['total']:.2f}",
            )

    def search_bill(keyword):

        find_bill_view.clear_table()

        bills = search_bill_history(keyword)

        bills.reverse()

        for bill in bills:

            find_bill_view.add_bill(
                bill["bill_no"],
                bill["date"],
                bill.get("payment_mode", "-"),
                len(bill["items"]),
                f"₹ {bill['total']:.2f}",
            )

    # =====================================================
    # View Switching Functions
    # =====================================================

    def show_billing_view():

        if product_view is not None:
            product_view.pack_forget()

        if settings_view is not None:
            settings_view.pack_forget()

        if find_bill_view is not None:
            find_bill_view.pack_forget()

        if billing_view is not None:
            billing_view.pack(
                fill="both",
                expand=True,
            )

        window.title("QuickBill System - Billing")

        if billing_view is not None:

            if scanner_active:

                billing_view.update_scanner_status("Scanner Active")

            else:

                billing_view.update_scanner_status("Ready")

    def show_products_view():

        if billing_view is not None:
            billing_view.pack_forget()

        if settings_view is not None:
            settings_view.pack_forget()

        if find_bill_view is not None:
            find_bill_view.pack_forget()

        if product_view is not None:

            product_view.refresh_table()

            product_view.pack(
                fill="both",
                expand=True,
            )

        window.title("QuickBill System - Product Master")

    def show_settings_view():

        if billing_view is not None:
            billing_view.pack_forget()

        if product_view is not None:
            product_view.pack_forget()

        if find_bill_view is not None:
            find_bill_view.pack_forget()

        if settings_view is not None:

            settings_view.pack(
                fill="both",
                expand=True,
            )

        window.title("QuickBill System - Settings")

    def show_find_bill_view():

        if billing_view is not None:
            billing_view.pack_forget()

        if product_view is not None:
            product_view.pack_forget()

        if settings_view is not None:
            settings_view.pack_forget()

        if find_bill_view is not None:

            find_bill_view.bill_search_var.set("")

            load_bill_history()

            find_bill_view.pack(
                fill="both",
                expand=True,
            )

        window.title("QuickBill System - Find Bill")

    find_bill_view = FindBillView(
        content_container,
        {
            "back": show_billing_view,
            "search": search_bill,
            "refresh": load_bill_history,
            "view": open_bill_details,
            "reprint": reprint_bill,
            "delete": delete_bill,
        },
    )

    toolbar = Toolbar(
        window,
        {
            "billing": show_billing_view,
            "new_bill": clear_cart_all,
            "save_bill": lambda: None,
            "print_bill": lambda: None,
            "hold_bill": hold_current_bill,
            "find_bill": lambda: show_find_bill_view(),
            "products": show_products_view,
            "settings": show_settings_view,
            "customers": lambda: None,
            "reports": lambda: None,
            "exit": close_application,
        },
    )

    # Pack toolbar at the bottom (but above status bar since status bar was packed side="bottom" first)
    toolbar.pack(side="bottom", fill="x")

    # =====================================================
    # Initialize
    # =====================================================

    show_billing_view()

    window.mainloop()
