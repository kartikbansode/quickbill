from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.barcode import code128
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime
import os
import json
from logic.billing import calculate_totals

# Register DejaVuSans fonts
try:
    pdfmetrics.registerFont(TTFont("DejaVuSans", "assets/fonts/DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "assets/fonts/DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", "assets/fonts/DejaVuSans-Oblique.ttf"))
except Exception as e:
    print(f"[ERROR] Failed to load DejaVuSans fonts: {e}")
    raise

def generate_pdf_bill(cart):
    bill_no = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    bill_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    # Ensure bills directory exists
    if not os.path.exists("bills"):
        os.makedirs("bills")
    
    # Create PDF
    pdf_file = f"bills/bill_{bill_no}.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name="Title", fontName="DejaVuSans-Bold", fontSize=18, alignment=1, spaceAfter=10)
    header_style = ParagraphStyle(name="Header", fontName="DejaVuSans", fontSize=10, alignment=0, spaceAfter=5)
    subheader_style = ParagraphStyle(name="SubHeader", fontName="DejaVuSans-Bold", fontSize=12, alignment=0, spaceAfter=5)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])
    totals_style = ParagraphStyle(name="Totals", fontName="DejaVuSans-Bold", fontSize=10, alignment=2, spaceBefore=10)
    footer_style = ParagraphStyle(name="Footer", fontName="DejaVuSans-Oblique", fontSize=8, alignment=1, spaceBefore=10)

    # Store Header
    elements.append(Paragraph("QuickBill Systems", title_style))
    elements.append(Paragraph("123 Retail Street, City, Country", header_style))
    elements.append(Paragraph("Phone: +123-456-7890 | Email: contact@quickbill.com", header_style))
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black, spaceBefore=5, spaceAfter=5))
    
    # Bill Details
    elements.append(Paragraph("Invoice", subheader_style))
    elements.append(Paragraph(f"Bill No: {bill_no}", header_style))
    elements.append(Paragraph(f"Date: {bill_date}", header_style))
    
    # Item Table
    data = [["Item", "Qty", "Price", "Total"]]
    for i, item in enumerate(cart):
        row_color = colors.lightgrey if i % 2 else colors.white
        table_style.add('BACKGROUND', (0, i+1), (-1, i+1), row_color)
        data.append([item["name"][:30], str(item["qty"]), f"₹ {item['price']:.2f}", f"₹ {item['total']:.2f}"])
    
    table = Table(data, colWidths=[3.5*inch, 0.8*inch, 1*inch, 1*inch])
    table.setStyle(table_style)
    elements.append(table)
    
    # Totals
    subtotal, tax, discount, total = calculate_totals()
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Subtotal: ₹ {subtotal:.2f}", totals_style))
    elements.append(Paragraph(f"Tax (18%): ₹ {tax:.2f}", totals_style))
    elements.append(Paragraph(f"Discount (5%): ₹ {discount:.2f}", totals_style))
    elements.append(Paragraph(f"Total: ₹ {total:.2f}", totals_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Barcode
    barcode = code128.Code128(bill_no, barHeight=0.6*inch, barWidth=0.02*inch)
    elements.append(barcode)
    
    # Footer
    elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black, spaceBefore=10, spaceAfter=5))
    elements.append(Paragraph("QuickBill Systems", footer_style))
    elements.append(Paragraph("Thank you for shopping with us!", footer_style))
    
    # Build PDF
    try:
        doc.build(elements)
    except Exception as e:
        print(f"[ERROR] Failed to build PDF: {e}")
        raise
    
    # Save to JSON
    bill = {
        "bill_no": bill_no,
        "date": bill_date,
        "items": [
            {"name": item["name"], "qty": item["qty"], "price": item["price"], "total": item["total"]}
            for item in cart
        ],
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "total": total
    }
    
    bills_history_file = "bills_history.json"
    bills = []
    if os.path.exists(bills_history_file):
        try:
            with open(bills_history_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    bills = json.load(f)
        except json.JSONDecodeError:
            print(f"[ERROR] Invalid JSON in {bills_history_file}, initializing empty list.")
    
    bills.append(bill)
    
    try:
        with open(bills_history_file, 'w', encoding='utf-8') as f:
            json.dump(bills, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to write to {bills_history_file}: {e}")
        raise