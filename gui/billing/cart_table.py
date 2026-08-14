import tkinter as tk
from tkinter import ttk
from gui.ui_components import ToolTip
from logic.config import get_currency

class CartTable(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self._increase_callback = None
        self._decrease_callback = None
        self._delete_callback = None
        
        self.row_buttons = {}

        columns = ("S.No", "Barcode", "Product", "Qty", "Rate", "Amount", "Actions")

        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=13)
        self.tree.heading("S.No", text="S.No")
        self.tree.heading("Barcode", text="Barcode")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Qty", text="Qty")
        self.tree.heading("Rate", text="Rate")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Actions", text="Actions")

        self.tree.column("S.No", width=60, anchor="center", stretch=False)
        self.tree.column("Barcode", width=140, anchor="center", stretch=False)
        self.tree.column("Product", width=300, stretch=True)
        self.tree.column("Qty", width=70, anchor="center", stretch=False)
        self.tree.column("Rate", width=90, anchor="center", stretch=False)
        self.tree.column("Amount", width=110, anchor="center", stretch=False)
        self.tree.column("Actions", width=100, anchor="center", stretch=False)

        def on_scroll(*args):
            self.tree.yview(*args)
            self.after(10, self.update_button_positions)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=on_scroll)
        self.tree.configure(yscrollcommand=lambda f, l: (scrollbar.set(f, l), self.after(10, self.update_button_positions)))

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<Delete>", lambda e: self.delete_item())
        
        self.tree.bind("<Configure>", lambda e: self.after(10, self.update_button_positions))
        self.tree.bind("<<TreeviewSelect>>", lambda e: self.after(10, self.update_button_positions))
        self.tree.bind("<MouseWheel>", lambda e: self.after(10, self.update_button_positions))

        self.empty_label = tk.Label(
            self,
            text="🛒\n\nCurrent Bill is Empty\n\nScan a barcode\nor\nType barcode manually and press Add",
            bg="white",
            fg="#808080",
            font=("Segoe UI", 12),
            justify="center",
        )
        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.tag_configure("odd", background="#F5F5F5")

        scrollbar.pack(side="right", fill="y")
        self.tree.pack_forget()
        self.empty_label.pack(expand=True, fill="both")

    def update_button_positions(self):
        if not self.tree.winfo_viewable():
            return
            
        for iid, (bp, bm, bd) in self.row_buttons.items():
            if self.tree.exists(iid):
                bbox = self.tree.bbox(iid, "Actions")
                if bbox:
                    x, y, w, h = bbox
                    if y < 0 or y + h > self.tree.winfo_height():
                        bp.place_forget()
                        bm.place_forget()
                        bd.place_forget()
                        continue
                        
                    btn_w = 26
                    gap = 2
                    start_x = x + (w - (3*btn_w + 2*gap)) // 2
                    
                    bp.place(in_=self.tree, x=start_x, y=y+2, width=btn_w, height=h-4)
                    bm.place(in_=self.tree, x=start_x + btn_w + gap, y=y+2, width=btn_w, height=h-4)
                    bd.place(in_=self.tree, x=start_x + 2*btn_w + 2*gap, y=y+2, width=btn_w, height=h-4)
                else:
                    bp.place_forget()
                    bm.place_forget()
                    bd.place_forget()

    def clear(self):
        for btns in self.row_buttons.values():
            for btn in btns:
                btn.destroy()
        self.row_buttons.clear()
        self.tree.delete(*self.tree.get_children())

    def set_actions(
        self, increase_callback=None, decrease_callback=None, delete_callback=None
    ):
        self._increase_callback = increase_callback
        self._decrease_callback = decrease_callback
        self._delete_callback = delete_callback

    def refresh_table(self, items):
        self.clear()

        if not items:
            self.tree.pack_forget()
            self.empty_label.pack(expand=True, fill="both")
            return

        self.empty_label.pack_forget()
        self.tree.pack(side="left", fill="both", expand=True)

        for index, item in enumerate(items):
            rate = item.get("selling_price", item.get("price", 0))
            tag = "even" if index % 2 == 0 else "odd"
            bg_color = "#FFFFFF" if index % 2 == 0 else "#F5F5F5"
            last_item_id = str(index)
            
            self.tree.insert(
                "", "end", iid=last_item_id,
                values=(
                    index + 1, item["barcode"], item["name"], item["qty"],
                    f"{get_currency()} {rate:.2f}", f"{get_currency()} {item['total']:.2f}", ""
                ),
                tags=(tag,)
            )
            
            bp = tk.Label(self.tree, text="➕", cursor="hand2", bg=bg_color, fg="#2563eb", font=("Segoe UI", 10))
            bm = tk.Label(self.tree, text="➖", cursor="hand2", bg=bg_color, fg="#475569", font=("Segoe UI", 10))
            bd = tk.Label(self.tree, text="🗑", cursor="hand2", bg=bg_color, fg="#dc2626", font=("Segoe UI", 10))
            
            def make_hover(btn, normal_bg, hover_bg, normal_fg, hover_fg):
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=hover_bg, fg=hover_fg))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=normal_bg, fg=normal_fg))
                
            make_hover(bp, bg_color, "#dbeafe", "#2563eb", "#1d4ed8")
            make_hover(bm, bg_color, "#f1f5f9", "#475569", "#334155")
            make_hover(bd, bg_color, "#fee2e2", "#dc2626", "#b91c1c")
            
            bp.bind("<Button-1>", lambda e, idx=index: self._increase_callback(idx) if self._increase_callback else None)
            bm.bind("<Button-1>", lambda e, idx=index: self._decrease_callback(idx) if self._decrease_callback else None)
            bd.bind("<Button-1>", lambda e, idx=index: self._delete_callback(idx) if self._delete_callback else None)
            
            ToolTip(bp, "Increase quantity")
            ToolTip(bm, "Decrease quantity")
            ToolTip(bd, "Remove item")
            
            self.row_buttons[last_item_id] = (bp, bm, bd)
            
        self.tree.see(last_item_id)
        self.after(20, self.update_button_positions)

    def add_item(self, barcode, product, qty, rate, amount):
        pass # add_item is deprecated in favor of refresh_table

    def selected(self):
        return self.tree.selection()

    def _selected_index(self):
        selection = self.selected()
        if not selection:
            return None
        try:
            return int(selection[0])
        except ValueError:
            return None

    def delete_item(self):
        index = self._selected_index()
        if index is not None and self._delete_callback:
            self._delete_callback(index)
