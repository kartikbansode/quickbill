# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox

cart = []

def launch_main_window():
    root = tk.Tk()
    root.title("QuickBill")
    root.geometry("800x600")

    # Header
    tk.Label(root, text="QuickBill - Billing System", font=("Arial", 20)).pack(pady=10)

    # Table for cart
    columns = ("Name", "Qty", "Price", "Total")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=20, fill="x", padx=20)

    # Dummy Add Button
    def add_dummy_item():
        cart.append(("Sample Item", 1, 100, 100))
        tree.insert("", tk.END, values=("Sample Item", 1, 100, 100))

    tk.Button(root, text="Add Dummy Item", command=add_dummy_item).pack()

    root.mainloop()
