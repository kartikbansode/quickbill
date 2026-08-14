import tkinter as tk
from tkinter import ttk, messagebox
from gui.ui_components import create_success_button, FONT_LABEL, FONT_SECTION


class SettingsView(tk.Frame):
    def __init__(self, parent, webcam_url="", upi_id="", company_info=None, billing_info=None, save_callback=None, save_payment_callback=None, save_business_callback=None, save_billing_callback=None):
        super().__init__(parent, bg="#f4f6f9")

        self.save_callback = save_callback
        self.save_payment_callback = save_payment_callback
        self.save_business_callback = save_business_callback
        self.save_billing_callback = save_billing_callback
        company_info = company_info or {}
        billing_info = billing_info or {}

        title = tk.Label(
            self,
            text="Settings",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f6f9",
            fg="#1f2937",
        )
        title.pack(anchor="w", padx=20, pady=(10, 5))

        # --- Create a Canvas and Scrollbar to allow scrolling if window is small ---
        self.canvas = tk.Canvas(self, bg="#f4f6f9", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f4f6f9")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.winfo_width())
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.bind("<Configure>", self.on_frame_configure)

        def _on_mousewheel(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_mouse(_):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            self.canvas.bind_all("<Button-4>", _on_mousewheel)
            self.canvas.bind_all("<Button-5>", _on_mousewheel)

        def _unbind_mouse(_):
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")

        self.canvas.bind("<Enter>", _bind_mouse)
        self.canvas.bind("<Leave>", _unbind_mouse)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # --- Scanner Settings ---
        scanner_frame = tk.LabelFrame(
            self.scrollable_frame,
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
        self.url_entry = tk.Entry(scanner_frame, textvariable=self.url_var, font=("Segoe UI", 10), width=60)
        self.url_entry.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="ew")

        save_scanner_btn = create_success_button(scanner_frame, text="Save", command=self.save_scanner_settings)
        save_scanner_btn.grid(row=1, column=1)
        scanner_frame.columnconfigure(0, weight=1)

        # --- Payment Settings ---
        payment_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Payment Settings",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            padx=15,
            pady=15,
        )
        payment_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(payment_frame, text="UPI ID", font=("Segoe UI", 10, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        tk.Label(payment_frame, text="UPI ID used to generate customer payment QR codes.", font=("Segoe UI", 9), fg="#6b7280", bg="white").grid(row=1, column=0, sticky="w", pady=(0, 10))

        self.upi_var = tk.StringVar(value=upi_id)
        self.upi_entry = tk.Entry(payment_frame, textvariable=self.upi_var, font=("Segoe UI", 10), width=60)
        self.upi_entry.grid(row=2, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")

        save_payment_btn = create_success_button(payment_frame, text="Save", command=self.save_payment_settings)
        save_payment_btn.grid(row=2, column=1, pady=(0, 10))
        payment_frame.columnconfigure(0, weight=1)

        # --- Business & Billing Information ---
        biz_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Business & Billing Information",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            padx=15,
            pady=15,
        )
        biz_frame.pack(fill="x", padx=20, pady=10)

        row_idx = 0

        # Helper function for adding fields
        def add_field(label_text, helper_text, var_name, value, is_multiline=False):
            nonlocal row_idx
            tk.Label(biz_frame, text=label_text, font=("Segoe UI", 10, "bold"), bg="white").grid(row=row_idx, column=0, sticky="w", pady=(5, 0))
            row_idx += 1
            if helper_text:
                tk.Label(biz_frame, text=helper_text, font=("Segoe UI", 9), fg="#6b7280", bg="white").grid(row=row_idx, column=0, sticky="w", pady=(0, 5))
                row_idx += 1
            
            if is_multiline:
                text_widget = tk.Text(biz_frame, font=("Segoe UI", 10), width=60, height=3)
                text_widget.insert("1.0", value)
                text_widget.grid(row=row_idx, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")
                setattr(self, var_name, text_widget)
            else:
                str_var = tk.StringVar(value=value)
                entry_widget = tk.Entry(biz_frame, textvariable=str_var, font=("Segoe UI", 10), width=60)
                entry_widget.grid(row=row_idx, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")
                setattr(self, var_name, str_var)
            
            row_idx += 1

        add_field("Cashier Name", "Name displayed on bills and used to identify the current cashier.", "cashier_var", company_info.get("cashier_name", ""))
        add_field("Company / Business Name", "Business name displayed on customer invoices and receipts.", "company_var", company_info.get("name", ""))
        add_field("Address", "", "address_var", company_info.get("address", ""), is_multiline=True)
        add_field("Phone", "", "phone_var", company_info.get("phone", ""))
        add_field("Email", "", "email_var", company_info.get("email", ""))
        add_field("GSTIN", "Optional GST registration number displayed on invoices.", "gst_var", company_info.get("gst", ""))

        save_biz_btn = create_success_button(biz_frame, text="Save", command=self.save_business_settings)
        save_biz_btn.grid(row=row_idx, column=0, pady=(10, 10), sticky="w")
        
        biz_frame.columnconfigure(0, weight=1)

        # --- Billing Preferences ---
        bill_frame = tk.LabelFrame(
            self.scrollable_frame,
            text="Billing Preferences",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#374151",
            padx=15,
            pady=15,
        )
        bill_frame.pack(fill="x", padx=20, pady=10)

        b_row_idx = 0

        def add_bill_field(label_text, helper_text, var_name, value, is_combobox=False, combo_values=None, is_checkbox=False):
            nonlocal b_row_idx
            tk.Label(bill_frame, text=label_text, font=("Segoe UI", 10, "bold"), bg="white", fg="#374151").grid(row=b_row_idx, column=0, sticky="w", pady=(10, 0))
            b_row_idx += 1
            if helper_text:
                tk.Label(bill_frame, text=helper_text, font=("Segoe UI", 9), fg="#6b7280", bg="white").grid(row=b_row_idx, column=0, sticky="w", pady=(0, 5))
                b_row_idx += 1
            
            if is_checkbox:
                var = tk.BooleanVar(value=value)
                chk = tk.Checkbutton(bill_frame, text="Enable Round Off", variable=var, bg="white", font=("Segoe UI", 10))
                chk.grid(row=b_row_idx, column=0, padx=(0, 10), pady=(0, 10), sticky="w")
                setattr(self, var_name, var)
            elif is_combobox:
                str_var = tk.StringVar(value=value)
                combo = ttk.Combobox(bill_frame, textvariable=str_var, font=("Segoe UI", 10), width=58, state="readonly", values=combo_values)
                combo.grid(row=b_row_idx, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")
                setattr(self, var_name, str_var)
            else:
                str_var = tk.StringVar(value=value)
                entry = tk.Entry(bill_frame, textvariable=str_var, font=("Segoe UI", 10), width=60)
                entry.grid(row=b_row_idx, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")
                setattr(self, var_name, str_var)
            b_row_idx += 1

        currencies = [
            "₹", "$", "€", "£", "¥", "A$", "C$", "CHF", "元", "kr",
            "NZ$", "₩", "S$", "R", "₽", "R$", "₺", "₱", "RM", "฿", "Rp"
        ]

        add_bill_field("Currency Symbol", "Select the primary currency symbol for your business.", "currency_var", billing_info.get("currency", "₹"), is_combobox=True, combo_values=currencies)
        add_bill_field("Invoice Prefix", "Prefix added before the generated invoice number (e.g. INV-20260810-001).", "prefix_var", billing_info.get("invoice_prefix", "INV"))
        add_bill_field("Round Off Total", "Automatically round the final invoice amount to the nearest whole number.", "round_off_var", billing_info.get("round_off", True), is_checkbox=True)

        save_bill_btn = create_success_button(bill_frame, text="Save", command=self.save_billing_settings)
        save_bill_btn.grid(row=b_row_idx, column=0, pady=(10, 10), sticky="w")
        
        bill_frame.columnconfigure(0, weight=1)

    def on_frame_configure(self, event):
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

    def save_scanner_settings(self):
        if self.save_callback:
            self.save_callback(self.url_var.get().strip())
            messagebox.showinfo("Settings", "Webcam URL saved successfully.")

    def save_payment_settings(self):
        upi_id = self.upi_var.get().strip()
        if self.save_payment_callback:
            self.save_payment_callback(upi_id)
            messagebox.showinfo("Settings", "UPI ID saved successfully.")

    def save_business_settings(self):
        company_info = {
            "cashier_name": self.cashier_var.get().strip(),
            "name": self.company_var.get().strip(),
            "address": self.address_var.get("1.0", tk.END).strip(),
            "phone": self.phone_var.get().strip(),
            "email": self.email_var.get().strip(),
            "gst": self.gst_var.get().strip(),
        }
        if self.save_business_callback:
            self.save_business_callback(company_info)
            messagebox.showinfo("Settings", "Business information saved successfully.")

    def save_billing_settings(self):
        billing_info = {
            "currency": self.currency_var.get().strip(),
            "invoice_prefix": self.prefix_var.get().strip(),
            "round_off": self.round_off_var.get(),
        }

        if self.save_billing_callback:
            self.save_billing_callback(billing_info)
            messagebox.showinfo("Settings", "Billing preferences saved successfully.")