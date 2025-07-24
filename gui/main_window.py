# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from logic.billing import add_to_cart, remove_from_cart, update_qty, calculate_totals, cart

def launch_main_window():
    root = tk.Tk()
    root.title("QuickBill")
    root.geometry("900x600")

    # Header
    tk.Label(root, text="QuickBill - Billing System", font=("Arial", 20)).pack(pady=10)

    # Cart table
    columns = ("Name", "Qty", "Price", "Total")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(pady=10)

    # Totals display
    totals_label = tk.Label(root, text="", font=("Arial", 12))
    totals_label.pack(pady=10)

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for item in cart:
            tree.insert("", tk.END, values=(item['name'], item['qty'], item['price'], item['total']))
        subtotal, tax, disc, total = calculate_totals()
        totals_label.config(text=f"Subtotal: ₹{subtotal:.2f} | Tax: ₹{tax:.2f} | Discount: ₹{disc:.2f} | Total: ₹{total:.2f}")

    # Add item manually
    def add_item_prompt():
        win = tk.Toplevel(root)
        win.title("Add Item")
        tk.Label(win, text="Item Name:").grid(row=0, column=0)
        tk.Label(win, text="Price:").grid(row=1, column=0)
        name_entry = tk.Entry(win)
        price_entry = tk.Entry(win)
        name_entry.grid(row=0, column=1)
        price_entry.grid(row=1, column=1)

        def add_and_close():
            try:
                name = name_entry.get()
                price = float(price_entry.get())
                add_to_cart(name, price)
                refresh_table()
                win.destroy()
            except:
                messagebox.showerror("Invalid", "Price must be a number")

        tk.Button(win, text="Add", command=add_and_close).grid(row=2, columnspan=2)

    # Change quantity
    def update_quantity():
        selected = tree.focus()
        if not selected:
            return
        item = tree.item(selected)['values']
        name = item[0]
        win = tk.Toplevel(root)
        win.title("Update Quantity")
        tk.Label(win, text=f"New Quantity for {name}:").pack()
        qty_entry = tk.Entry(win)
        qty_entry.pack()

        def update_and_close():
            try:
                qty = int(qty_entry.get())
                if qty <= 0:
                    remove_from_cart(name)
                else:
                    update_qty(name, qty)
                refresh_table()
                win.destroy()
            except:
                messagebox.showerror("Invalid", "Enter valid number")

        tk.Button(win, text="Update", command=update_and_close).pack()

    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="➕ Add Item", command=add_item_prompt).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="✏️ Change Qty", command=update_quantity).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="🗑️ Remove Item", command=lambda: remove_from_cart_prompt()).grid(row=0, column=2, padx=10)

    # Remove item
    def remove_from_cart_prompt():
        selected = tree.focus()
        if not selected:
            return
        item = tree.item(selected)['values']
        remove_from_cart(item[0])
        refresh_table()

    refresh_table()
    root.mainloop()
