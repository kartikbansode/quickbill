from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from tkinter import messagebox
import os

def generate_pdf_bill(cart, company_info=None):
    if company_info is None:
        company_info = {
            "name": "QuickBill Pvt. Ltd.",
            "address": "Street no. 231 , City, State, 100138",
            "phone": "999-888-7777",
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

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, company_info["name"])

    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, company_info["address"])
    y -= 15
    c.drawString(50, y, f"Phone: {company_info['phone']} | GST: {company_info['gst']}")
    y -= 30
    c.drawString(50, y, f"Bill No: {bill_no}")
    c.drawString(300, y, f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Qty")
    c.drawString(300, y, "Price")
    c.drawString(400, y, "Total")
    y -= 20

    c.setFont("Helvetica", 10)
    subtotal = 0

    for item in cart:
        c.drawString(50, y, item["name"])
        c.drawString(250, y, str(item["qty"]))
        c.drawString(300, y, f"{item['price']:.2f}")
        c.drawString(400, y, f"{item['total']:.2f}")
        subtotal += item["total"]
        y -= 15

    tax = subtotal * 0.18
    discount = subtotal * 0.05
    total = subtotal + tax - discount

    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(300, y, "Subtotal:")
    c.drawString(400, y, f"{subtotal:.2f}")
    y -= 15
    c.drawString(300, y, "Tax (18%):")
    c.drawString(400, y, f"{tax:.2f}")
    y -= 15
    c.drawString(300, y, "Discount (5%):")
    c.drawString(400, y, f"-{discount:.2f}")
    y -= 15
    c.drawString(300, y, "Total:")
    c.drawString(400, y, f"{total:.2f}")

    c.save()
    messagebox.showinfo("Bill Generated", f"Bill saved successfully to:\n{filepath}")




