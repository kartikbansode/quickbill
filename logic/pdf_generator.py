from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode import code128
from datetime import datetime
from tkinter import messagebox
import os
import textwrap
from reportlab.graphics.barcode import code128

# Font configuration
FONT_PATH = "assets/fonts/DejaVuSans.ttf"
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont("DejaVuSans", FONT_PATH))
    FONT = "DejaVuSans"
else:
    print("⚠️ DejaVuSans.ttf not found. Using Helvetica.")
    FONT = "Helvetica"

def format_currency(value):
    return f"₹{value:.2f}"

def wrap_text(text, max_chars):
    return textwrap.wrap(text, width=max_chars)

def generate_pdf_bill(cart, customer_name="Customer", customer_mobile="N/A", company_info=None):
    if company_info is None:
        company_info = {
            "name": "QuickBill Pvt. Ltd.",
            "address": "231 Market Street, City, State - 100138",
            "phone": "+91-9998887777",
            "gst": "GSTIN1234567890"
        }

    now = datetime.now()
    bill_no = now.strftime("%Y%m%d%H%M%S")
    filename = f"bill_{bill_no}.pdf"
    folder = "bills"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin

    # Header
    c.setFont(FONT, 16)
    c.drawString(margin, y, company_info["name"])
    c.setFont(FONT, 10)
    y -= 20
    c.drawString(margin, y, company_info["address"])
    y -= 15
    c.drawString(margin, y, f"Phone: {company_info['phone']} | GSTIN: {company_info['gst']}")

    # Bill Info
    y -= 30
    c.line(margin, y + 15, width - margin, y + 15)
    c.setFont(FONT, 10)
    c.drawString(margin, y, f"Bill No: {bill_no}")
    c.drawString(margin + 300, y, f"Date: {now.strftime('%d-%m-%Y %I:%M %p')}")
    c.line(margin, y - 5, width - margin, y - 5)
    y -= 30

    # Table Header
    c.setFont(FONT, 11)
    c.drawString(margin, y, "Item")
    c.drawString(margin + 300, y, "Qty")
    c.drawString(margin + 340, y, "Price")
    c.drawString(margin + 420, y, "Total")
    y -= 5
    c.line(margin, y, width - margin, y)
    y -= 15

    # Table Content
    c.setFont(FONT, 10)
    subtotal = 0
    row_height = 15
    for item in cart:
        if y < 120:
            c.showPage()
            y = height - 100

        wrapped_lines = wrap_text(item["name"], 45)
        for i, line in enumerate(wrapped_lines):
            c.drawString(margin, y, line)
            if i == 0:
                c.drawString(margin + 300, y, str(item["qty"]))
                c.drawString(margin + 340, y, format_currency(item["price"]))
                c.drawString(margin + 420, y, format_currency(item["total"]))
            y -= row_height
        subtotal += item["total"]

    # Totals
    tax = round(subtotal * 0.18, 2)
    discount = round(subtotal * 0.05, 2)
    total = round(subtotal + tax - discount, 2)

    y -= 10
    c.line(margin + 250, y, width - margin, y)
    y -= row_height
    c.drawString(margin + 250, y, "Subtotal:")
    c.drawString(margin + 380, y, format_currency(subtotal))
    y -= row_height
    c.drawString(margin + 250, y, "GST (18%):")
    c.drawString(margin + 380, y, format_currency(tax))
    y -= row_height
    c.drawString(margin + 250, y, "Discount (5%):")
    c.drawString(margin + 380, y, f"-{format_currency(discount)}")
    y -= row_height
    # Grand Total (larger font)
    c.setFont(FONT, 11)
    c.drawString(margin + 250, y, "Grand Total:")
    c.setFont(FONT, 14)
    c.drawString(margin + 380, y, format_currency(total))
    y -= 10
    c.line(margin + 250, y, width - margin, y)

    # Barcode Below Totals (clean placement)
    y -= 40
    c.setFont(FONT, 10)
    c.drawString(margin, y + 10, "")
    barcode = code128.Code128(bill_no, barHeight=30, barWidth=1.2)
    barcode.drawOn(c, margin + 50, y)

    # Footer
    y -= 60
    c.setFont(FONT, 10)
    c.drawCentredString(width / 2, y, "Thank you for shopping with QuickBill!")
    y -= 15
    c.setFont(FONT, 8)
    c.drawCentredString(width / 2, y, "This is a computer-generated bill and does not require a signature.")

    c.save()
    messagebox.showinfo("Bill Generated", f"Bill saved successfully to:\n{filepath}")
