import datetime
import json
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    HRFlowable,
    KeepTogether,
)
from reportlab.graphics.barcode.code128 import Code128
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from logic.billing import calculate_totals
from logic.config import get
from logic.file_paths import data_path
from logic.resource_path import resource_path

# ============================================================
# Paths
# ============================================================

BILL_FOLDER = data_path("bills")

os.makedirs(
    BILL_FOLDER,
    exist_ok=True,
)


# ============================================================
# Fonts
# ============================================================

try:

    pdfmetrics.registerFont(
        TTFont(
            "DejaVuSans",
            resource_path("assets/fonts/DejaVuSans.ttf"),
        )
    )

    pdfmetrics.registerFont(
        TTFont(
            "DejaVuSans-Bold",
            resource_path("assets/fonts/DejaVuSans-Bold.ttf"),
        )
    )

    pdfmetrics.registerFont(
        TTFont(
            "DejaVuSans-Oblique",
            resource_path("assets/fonts/DejaVuSans-Oblique.ttf"),
        )
    )

except Exception as e:

    print(f"[ERROR] Failed to load PDF fonts: {e}")

    raise


# ============================================================
# Helpers
# ============================================================


def _safe_float(value, default=0.0):

    try:
        return float(value)

    except (
        TypeError,
        ValueError,
    ):
        return default


def _safe_int(value, default=0):

    try:
        return int(value)

    except (
        TypeError,
        ValueError,
    ):
        return default


def _currency(value):

    currency = "₹"

    try:
        currency = (
            get(
                "billing",
                "currency",
            )
            or "₹"
        )

    except Exception:
        pass

    return f"{currency} {_safe_float(value):,.2f}"


def _company_value(
    key,
    default="",
):

    try:

        value = get(
            "company",
            key,
        )

        if value is None:
            return default

        return str(value)

    except Exception:

        return default


def _billing_value(
    key,
    default=None,
):

    try:
        return get(
            "billing",
            key,
        )

    except Exception:

        return default


def _bill_paths(bill_no):

    bill_no = str(bill_no)

    a4_path = os.path.join(
        BILL_FOLDER,
        f"{bill_no}_A4.pdf",
    )

    thermal_path = os.path.join(
        BILL_FOLDER,
        f"{bill_no}_80mm.pdf",
    )

    return a4_path, thermal_path


# ============================================================
# Styles
# ============================================================


def _create_styles():

    return {
        "a4_title": ParagraphStyle(
            "A4Title",
            fontName="DejaVuSans-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=3 * mm,
        ),
        "a4_company": ParagraphStyle(
            "A4Company",
            fontName="DejaVuSans-Bold",
            fontSize=13,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
        ),
        "a4_small": ParagraphStyle(
            "A4Small",
            fontName="DejaVuSans",
            fontSize=8.5,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
        ),
        "a4_label": ParagraphStyle(
            "A4Label",
            fontName="DejaVuSans-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#6b7280"),
        ),
        "a4_value": ParagraphStyle(
            "A4Value",
            fontName="DejaVuSans-Bold",
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#111827"),
        ),
        "a4_item": ParagraphStyle(
            "A4Item",
            fontName="DejaVuSans",
            fontSize=8.5,
            leading=11,
            alignment=TA_LEFT,
        ),
        "a4_item_bold": ParagraphStyle(
            "A4ItemBold",
            fontName="DejaVuSans-Bold",
            fontSize=8.5,
            leading=11,
            alignment=TA_LEFT,
        ),
        "a4_item_header": ParagraphStyle(
            "A4ItemHeader",
            fontName="DejaVuSans-Bold",
            fontSize=8.5,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
        "a4_item_header_left": ParagraphStyle(
            "A4ItemHeaderLeft",
            fontName="DejaVuSans-Bold",
            fontSize=8.5,
            leading=11,
            alignment=TA_LEFT,
            textColor=colors.white,
        ),
        "a4_total_label": ParagraphStyle(
            "A4TotalLabel",
            fontName="DejaVuSans",
            fontSize=9,
            leading=12,
            alignment=TA_RIGHT,
        ),
        "a4_total": ParagraphStyle(
            "A4Total",
            fontName="DejaVuSans-Bold",
            fontSize=10,
            leading=13,
            alignment=TA_RIGHT,
        ),
        "a4_grand_total": ParagraphStyle(
            "A4GrandTotal",
            fontName="DejaVuSans-Bold",
            fontSize=15,
            leading=18,
            alignment=TA_RIGHT,
            textColor=colors.HexColor("#15803d"),
        ),
        "a4_footer": ParagraphStyle(
            "A4Footer",
            fontName="DejaVuSans-Oblique",
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#6b7280"),
        ),
        "thermal_company": ParagraphStyle(
            "ThermalCompany",
            fontName="DejaVuSans-Bold",
            fontSize=12,
            leading=14,
            alignment=TA_CENTER,
        ),
        "thermal_title": ParagraphStyle(
            "ThermalTitle",
            fontName="DejaVuSans-Bold",
            fontSize=11,
            leading=13,
            alignment=TA_CENTER,
        ),
        "thermal_text": ParagraphStyle(
            "ThermalText",
            fontName="DejaVuSans",
            fontSize=7.5,
            leading=9.5,
            alignment=TA_LEFT,
        ),
        "thermal_bold": ParagraphStyle(
            "ThermalBold",
            fontName="DejaVuSans-Bold",
            fontSize=7.5,
            leading=9.5,
        ),
        "thermal_center": ParagraphStyle(
            "ThermalCenter",
            fontName="DejaVuSans",
            fontSize=7.5,
            leading=9.5,
            alignment=TA_CENTER,
        ),
        "thermal_total": ParagraphStyle(
            "ThermalTotal",
            fontName="DejaVuSans-Bold",
            fontSize=9,
            leading=11,
            alignment=TA_RIGHT,
        ),
        "thermal_grand": ParagraphStyle(
            "ThermalGrand",
            fontName="DejaVuSans-Bold",
            fontSize=12,
            leading=14,
            alignment=TA_RIGHT,
        ),
        "thermal_footer": ParagraphStyle(
            "ThermalFooter",
            fontName="DejaVuSans-Oblique",
            fontSize=7,
            leading=9,
            alignment=TA_CENTER,
        ),
    }


# ============================================================
# Common bill data
# ============================================================


def _prepare_bill_data(
    cart,
    bill_no,
    payment_mode,
    received_amount,
    cashier,
):

    tax_percent = _billing_value(
        "tax_percent",
        10,
    )

    discount_percent = _billing_value(
        "discount_percent",
        5,
    )

    subtotal, tax, discount, total = calculate_totals(
        cart,
        tax_percent=tax_percent,
        discount_percent=discount_percent,
    )

    received_amount = _safe_float(received_amount)

    balance = received_amount - total

    bill_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    items = []

    for item in cart:

        price = _safe_float(
            item.get(
                "price",
                item.get(
                    "selling_price",
                    0,
                ),
            )
        )

        qty = _safe_int(
            item.get(
                "qty",
                0,
            )
        )

        item_total = _safe_float(
            item.get(
                "total",
                price * qty,
            )
        )

        items.append(
            {
                "barcode": item.get(
                    "barcode",
                    "",
                ),
                "sku": item.get(
                    "sku",
                    "",
                ),
                "name": item.get(
                    "name",
                    "",
                ),
                "brand": item.get(
                    "brand",
                    "",
                ),
                "category": item.get(
                    "category",
                    "",
                ),
                "qty": qty,
                "price": price,
                "selling_price": price,
                "mrp": _safe_float(
                    item.get(
                        "mrp",
                        0,
                    )
                ),
                "gst": item.get(
                    "gst",
                    0,
                ),
                "total": item_total,
            }
        )

    bill = {
        "bill_no": str(bill_no),
        "date": bill_date,
        "payment_mode": payment_mode,
        "received_amount": received_amount,
        "balance": balance,
        "cashier": cashier,
        "status": "PAID",
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "total": total,
    }

    return bill


# ============================================================
# A4 PDF
# ============================================================


def _generate_a4_pdf(
    bill,
    pdf_file,
):

    styles = _create_styles()

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
        title=f"QuickBill - {bill['bill_no']}",
        author=_company_value(
            "name",
            "QuickBill",
        ),
    )

    elements = []

    company_name = _company_value(
        "name",
        "QuickBill",
    )

    owner = _company_value(
        "owner",
        "",
    )

    address = _company_value(
        "address",
        "",
    )

    phone = _company_value(
        "phone",
        "",
    )

    email = _company_value(
        "email",
        "",
    )

    gst_no = _company_value(
        "gst",
        "",
    )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    elements.append(
        Paragraph(
            company_name,
            styles["a4_company"],
        )
    )

    if owner:

        elements.append(
            Paragraph(
                owner,
                styles["a4_small"],
            )
        )

    contact_parts = []

    if address:
        contact_parts.append(address)

    if phone:
        contact_parts.append(f"Phone: {phone}")

    if email:
        contact_parts.append(f"Email: {email}")

    if gst_no:
        contact_parts.append(f"GSTIN: {gst_no}")

    if contact_parts:

        elements.append(
            Paragraph(
                " | ".join(contact_parts),
                styles["a4_small"],
            )
        )

    elements.append(
        Spacer(
            1,
            5 * mm,
        )
    )

    elements.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#1f2937"),
            spaceBefore=1 * mm,
            spaceAfter=4 * mm,
        )
    )

    elements.append(
        Paragraph(
            "TAX INVOICE",
            styles["a4_title"],
        )
    )

    # --------------------------------------------------------
    # Invoice information
    # --------------------------------------------------------

    info_data = [
        [
            Paragraph(
                "BILL NUMBER",
                styles["a4_label"],
            ),
            Paragraph(
                "DATE & TIME",
                styles["a4_label"],
            ),
            Paragraph(
                "PAYMENT",
                styles["a4_label"],
            ),
            Paragraph(
                "CASHIER",
                styles["a4_label"],
            ),
        ],
        [
            Paragraph(
                bill["bill_no"],
                styles["a4_value"],
            ),
            Paragraph(
                bill["date"],
                styles["a4_value"],
            ),
            Paragraph(
                str(bill["payment_mode"]),
                styles["a4_value"],
            ),
            Paragraph(
                str(bill["cashier"]),
                styles["a4_value"],
            ),
        ],
    ]

    info_table = Table(
        info_data,
        colWidths=[
            40 * mm,
            55 * mm,
            40 * mm,
            40 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#f8fafc"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#d1d5db"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#e5e7eb"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, 0),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    3,
                ),
                (
                    "TOPPADDING",
                    (0, 1),
                    (-1, 1),
                    3,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 1),
                    (-1, 1),
                    7,
                ),
            ]
        )
    )

    elements.append(info_table)

    elements.append(
        Spacer(
            1,
            6 * mm,
        )
    )

    # --------------------------------------------------------
    # Items table
    # --------------------------------------------------------

    item_data = [
        [
            Paragraph(
                "Item",
                styles["a4_item_header_left"],
            ),
            Paragraph(
                "Barcode",
                styles["a4_item_header"],
            ),
            Paragraph(
                "Qty",
                styles["a4_item_header"],
            ),
            Paragraph(
                "Rate",
                styles["a4_item_header"],
            ),
            Paragraph(
                "GST",
                styles["a4_item_header"],
            ),
            Paragraph(
                "Amount",
                styles["a4_item_header"],
            ),
        ]
    ]

    for item in bill["items"]:

        item_data.append(
            [
                Paragraph(
                    str(item["name"]),
                    styles["a4_item"],
                ),
                Paragraph(
                    str(item["barcode"]),
                    styles["a4_item"],
                ),
                Paragraph(
                    str(item["qty"]),
                    styles["a4_item"],
                ),
                Paragraph(
                    _currency(item["price"]),
                    styles["a4_item"],
                ),
                Paragraph(
                    f"{item['gst']}%",
                    styles["a4_item"],
                ),
                Paragraph(
                    _currency(item["total"]),
                    styles["a4_item"],
                ),
            ]
        )

    item_table = Table(
        item_data,
        colWidths=[
            55 * mm,
            31 * mm,
            15 * mm,
            26 * mm,
            18 * mm,
            33 * mm,
        ],
        repeatRows=1,
    )

    item_style_commands = [
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#1f2937"),
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white,
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.4,
            colors.HexColor("#d1d5db"),
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE",
        ),
        (
            "ALIGN",
            (1, 1),
            (-1, -1),
            "CENTER",
        ),
        (
            "ALIGN",
            (-1, 1),
            (-1, -1),
            "RIGHT",
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, 0),
            7,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, 0),
            7,
        ),
        (
            "TOPPADDING",
            (0, 1),
            (-1, -1),
            6,
        ),
        (
            "BOTTOMPADDING",
            (0, 1),
            (-1, -1),
            6,
        ),
    ]

    for index in range(
        1,
        len(item_data),
    ):

        if index % 2 == 0:

            item_style_commands.append(
                (
                    "BACKGROUND",
                    (0, index),
                    (-1, index),
                    colors.HexColor("#f8fafc"),
                )
            )

    item_table.setStyle(TableStyle(item_style_commands))

    elements.append(item_table)

    # --------------------------------------------------------
    # Totals
    # --------------------------------------------------------

    elements.append(
        Spacer(
            1,
            6 * mm,
        )
    )

    totals_data = [
        [
            "",
            Paragraph(
                "Subtotal",
                styles["a4_total_label"],
            ),
            Paragraph(
                _currency(bill["subtotal"]),
                styles["a4_total"],
            ),
        ],
        [
            "",
            Paragraph(
                "Tax",
                styles["a4_total_label"],
            ),
            Paragraph(
                _currency(bill["tax"]),
                styles["a4_total"],
            ),
        ],
        [
            "",
            Paragraph(
                "Discount",
                styles["a4_total_label"],
            ),
            Paragraph(
                f"- {_currency(bill['discount'])}",
                styles["a4_total"],
            ),
        ],
        [
            "",
            Paragraph(
                "Grand Total",
                styles["a4_total"],
            ),
            Paragraph(
                _currency(bill["total"]),
                styles["a4_grand_total"],
            ),
        ],
    ]

    totals_table = Table(
        totals_data,
        colWidths=[
            85 * mm,
            45 * mm,
            45 * mm,
        ],
    )

    totals_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "LINEABOVE",
                    (1, 3),
                    (-1, 3),
                    0.8,
                    colors.HexColor("#9ca3af"),
                ),
                (
                    "BACKGROUND",
                    (1, 3),
                    (-1, 3),
                    colors.HexColor("#f0fdf4"),
                ),
            ]
        )
    )

    elements.append(totals_table)

    # --------------------------------------------------------
    # Payment details
    # --------------------------------------------------------

    elements.append(
        Spacer(
            1,
            4 * mm,
        )
    )

    payment_data = [
        [
            Paragraph(
                "Received Amount",
                styles["a4_total_label"],
            ),
            Paragraph(
                _currency(bill["received_amount"]),
                styles["a4_total"],
            ),
        ],
        [
            Paragraph(
                "Balance / Change",
                styles["a4_total_label"],
            ),
            Paragraph(
                _currency(bill["balance"]),
                styles["a4_total"],
            ),
        ],
    ]

    payment_table = Table(
        payment_data,
        colWidths=[
            130 * mm,
            45 * mm,
        ],
    )

    payment_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    elements.append(payment_table)

    elements.append(
        Spacer(
            1,
            7 * mm,
        )
    )

    # --------------------------------------------------------
    # Bill barcode
    # --------------------------------------------------------

    barcode = Code128(
        str(bill["bill_no"]),
        barHeight=15 * mm,
        barWidth=0.38 * mm,
        humanReadable=False,
    )

    barcode_table = Table(
        [[barcode]],
        colWidths=[175 * mm],
    )

    barcode_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (0, 0),
                    "CENTER",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (0, 0),
                    "MIDDLE",
                ),
            ]
        )
    )

    elements.append(barcode_table)

    elements.append(
        Spacer(
            1,
            4 * mm,
        )
    )

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    elements.append(
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=colors.HexColor("#9ca3af"),
            spaceBefore=2 * mm,
            spaceAfter=3 * mm,
        )
    )

    elements.append(
        Paragraph(
            "Thank you for shopping with us!",
            styles["a4_footer"],
        )
    )

    elements.append(
        Paragraph(
            f"Generated by {company_name} • QuickBill",
            styles["a4_footer"],
        )
    )

    doc.build(elements)

    return pdf_file


# ============================================================
# 80mm Thermal PDF
# ============================================================


def _generate_80mm_pdf(
    bill,
    pdf_file,
):

    styles = _create_styles()

    # 80mm printer paper.
    # A sufficiently long page allows normal bills to fit
    # without making the content unnecessarily compressed.
    page_width = 80 * mm
    page_height = 250 * mm

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=(
            page_width,
            page_height,
        ),
        leftMargin=4 * mm,
        rightMargin=4 * mm,
        topMargin=5 * mm,
        bottomMargin=5 * mm,
        title=f"QuickBill - {bill['bill_no']}",
        author=_company_value(
            "name",
            "QuickBill",
        ),
    )

    elements = []

    company_name = _company_value(
        "name",
        "QuickBill",
    )

    address = _company_value(
        "address",
        "",
    )

    phone = _company_value(
        "phone",
        "",
    )

    gst_no = _company_value(
        "gst",
        "",
    )

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    elements.append(
        Paragraph(
            company_name,
            styles["thermal_company"],
        )
    )

    if address:

        elements.append(
            Paragraph(
                address,
                styles["thermal_center"],
            )
        )

    if phone:

        elements.append(
            Paragraph(
                f"Phone: {phone}",
                styles["thermal_center"],
            )
        )

    if gst_no:

        elements.append(
            Paragraph(
                f"GSTIN: {gst_no}",
                styles["thermal_center"],
            )
        )

    elements.append(
        Spacer(
            1,
            2 * mm,
        )
    )

    elements.append(
        HRFlowable(
            width="100%",
            thickness=0.6,
            color=colors.black,
            spaceBefore=1 * mm,
            spaceAfter=2 * mm,
        )
    )

    elements.append(
        Paragraph(
            "TAX INVOICE",
            styles["thermal_title"],
        )
    )

    elements.append(
        Spacer(
            1,
            2 * mm,
        )
    )

    # --------------------------------------------------------
    # Bill details
    # --------------------------------------------------------

    detail_data = [
        [
            Paragraph(
                "<b>Bill No:</b>",
                styles["thermal_text"],
            ),
            Paragraph(
                str(bill["bill_no"]),
                styles["thermal_text"],
            ),
        ],
        [
            Paragraph(
                "<b>Date:</b>",
                styles["thermal_text"],
            ),
            Paragraph(
                str(bill["date"]),
                styles["thermal_text"],
            ),
        ],
        [
            Paragraph(
                "<b>Payment:</b>",
                styles["thermal_text"],
            ),
            Paragraph(
                str(bill["payment_mode"]),
                styles["thermal_text"],
            ),
        ],
        [
            Paragraph(
                "<b>Cashier:</b>",
                styles["thermal_text"],
            ),
            Paragraph(
                str(bill["cashier"]),
                styles["thermal_text"],
            ),
        ],
    ]

    detail_table = Table(
        detail_data,
        colWidths=[
            19 * mm,
            53 * mm,
        ],
    )

    detail_table.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
            ]
        )
    )

    elements.append(detail_table)

    elements.append(
        Spacer(
            1,
            2 * mm,
        )
    )

    elements.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.black,
            spaceBefore=1 * mm,
            spaceAfter=2 * mm,
        )
    )

    # --------------------------------------------------------
    # Items
    # --------------------------------------------------------

    item_data = [
        [
            Paragraph(
                "<b>Item</b>",
                styles["thermal_text"],
            ),
            Paragraph(
                "<b>Qty</b>",
                styles["thermal_center"],
            ),
            Paragraph(
                "<b>Rate</b>",
                styles["thermal_center"],
            ),
            Paragraph(
                "<b>Amount</b>",
                styles["thermal_center"],
            ),
        ]
    ]

    for item in bill["items"]:

        name = str(item["name"])

        qty = _safe_int(item["qty"])

        rate = _safe_float(item["price"])

        amount = _safe_float(item["total"])

        item_data.append(
            [
                Paragraph(
                    name,
                    styles["thermal_text"],
                ),
                Paragraph(
                    str(qty),
                    styles["thermal_center"],
                ),
                Paragraph(
                    _currency(rate),
                    styles["thermal_center"],
                ),
                Paragraph(
                    _currency(amount),
                    styles["thermal_center"],
                ),
            ]
        )

    item_table = Table(
        item_data,
        colWidths=[
            34 * mm,
            9 * mm,
            15 * mm,
            18 * mm,
        ],
        repeatRows=1,
    )

    item_table.setStyle(
        TableStyle(
            [
                (
                    "LINEABOVE",
                    (0, 0),
                    (-1, 0),
                    0.5,
                    colors.black,
                ),
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, 0),
                    0.5,
                    colors.black,
                ),
                (
                    "LINEBELOW",
                    (0, -1),
                    (-1, -1),
                    0.5,
                    colors.black,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (-1, -1),
                    "RIGHT",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    2,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    2,
                ),
            ]
        )
    )

    elements.append(item_table)

    elements.append(
        Spacer(
            1,
            3 * mm,
        )
    )

    # --------------------------------------------------------
    # Totals
    # --------------------------------------------------------

    totals_data = [
        [
            Paragraph(
                "Subtotal",
                styles["thermal_text"],
            ),
            Paragraph(
                _currency(bill["subtotal"]),
                styles["thermal_total"],
            ),
        ],
        [
            Paragraph(
                "Tax",
                styles["thermal_text"],
            ),
            Paragraph(
                _currency(bill["tax"]),
                styles["thermal_total"],
            ),
        ],
        [
            Paragraph(
                "Discount",
                styles["thermal_text"],
            ),
            Paragraph(
                f"- {_currency(bill['discount'])}",
                styles["thermal_total"],
            ),
        ],
    ]

    totals_table = Table(
        totals_data,
        colWidths=[
            45 * mm,
            27 * mm,
        ],
    )

    totals_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
            ]
        )
    )

    elements.append(totals_table)

    elements.append(
        HRFlowable(
            width="100%",
            thickness=0.7,
            color=colors.black,
            spaceBefore=2 * mm,
            spaceAfter=2 * mm,
        )
    )

    grand_total_table = Table(
        [
            [
                Paragraph(
                    "GRAND TOTAL",
                    styles["thermal_total"],
                ),
                Paragraph(
                    _currency(bill["total"]),
                    styles["thermal_grand"],
                ),
            ]
        ],
        colWidths=[
            40 * mm,
            32 * mm,
        ],
    )

    grand_total_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (1, 0),
                    (1, 0),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#f3f4f6"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    colors.HexColor("#9ca3af"),
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
            ]
        )
    )

    elements.append(grand_total_table)

    elements.append(
        Spacer(
            1,
            2 * mm,
        )
    )

    # --------------------------------------------------------
    # Received / balance
    # --------------------------------------------------------

    payment_data = [
        [
            Paragraph(
                "Received",
                styles["thermal_text"],
            ),
            Paragraph(
                _currency(bill["received_amount"]),
                styles["thermal_total"],
            ),
        ],
        [
            Paragraph(
                "Balance / Change",
                styles["thermal_text"],
            ),
            Paragraph(
                _currency(bill["balance"]),
                styles["thermal_total"],
            ),
        ],
    ]

    payment_table = Table(
        payment_data,
        colWidths=[
            45 * mm,
            27 * mm,
        ],
    )

    payment_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    1,
                ),
            ]
        )
    )

    elements.append(payment_table)

    elements.append(
        Spacer(
            1,
            4 * mm,
        )
    )

    # --------------------------------------------------------
    # Barcode
    # --------------------------------------------------------

    barcode = Code128(
        str(bill["bill_no"]),
        barHeight=10 * mm,
        barWidth=0.28 * mm,
        humanReadable=False,
    )

    barcode_table = Table(
        [[barcode]],
        colWidths=[72 * mm],
    )

    barcode_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (0, 0),
                    "CENTER",
                ),
            ]
        )
    )

    elements.append(barcode_table)

    elements.append(
        Spacer(
            1,
            2 * mm,
        )
    )

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    elements.append(
        HRFlowable(
            width="100%",
            thickness=0.5,
            color=colors.black,
            spaceBefore=1 * mm,
            spaceAfter=2 * mm,
        )
    )

    elements.append(
        Paragraph(
            "Thank you for shopping with us!",
            styles["thermal_footer"],
        )
    )

    elements.append(
        Paragraph(
            f"Powered by QuickBill",
            styles["thermal_footer"],
        )
    )

    doc.build(elements)

    return pdf_file


# ============================================================
# Save Bill History
# ============================================================


def _save_bill_history(bill):

    history_file = data_path("bills_history.json")

    bills = []

    try:

        if os.path.exists(history_file):

            with open(
                history_file,
                "r",
                encoding="utf-8",
            ) as file:

                try:

                    bills = json.load(file)

                except (
                    json.JSONDecodeError,
                    ValueError,
                ):

                    bills = []

        if not isinstance(
            bills,
            list,
        ):
            bills = []

        # Prevent accidental duplicate bill numbers.
        existing_numbers = {
            str(
                item.get(
                    "bill_no",
                    "",
                )
            )
            for item in bills
            if isinstance(
                item,
                dict,
            )
        }

        if str(bill["bill_no"]) in existing_numbers:

            return

        bills.append(bill)

        os.makedirs(
            os.path.dirname(history_file),
            exist_ok=True,
        )

        with open(
            history_file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                bills,
                file,
                indent=4,
                ensure_ascii=False,
            )

    except Exception as e:

        print(f"[ERROR] Failed to save bill history: {e}")

        raise


# ============================================================
# Main Public Function
# ============================================================


def generate_pdf_bill(
    cart,
    bill_no,
    payment_mode,
    received_amount,
    cashier="Admin",
    save_history=True,
):

    if not cart:

        raise ValueError("Cannot generate an invoice for an empty cart.")

    os.makedirs(
        BILL_FOLDER,
        exist_ok=True,
    )

    bill = _prepare_bill_data(
        cart=cart,
        bill_no=bill_no,
        payment_mode=payment_mode,
        received_amount=received_amount,
        cashier=cashier,
    )

    a4_path, thermal_path = _bill_paths(bill_no)

    # --------------------------------------------------------
    # Generate A4
    # --------------------------------------------------------

    _generate_a4_pdf(
        bill,
        a4_path,
    )

    # --------------------------------------------------------
    # Generate 80mm
    # --------------------------------------------------------

    _generate_80mm_pdf(
        bill,
        thermal_path,
    )

    # --------------------------------------------------------
    # Save history exactly once
    # --------------------------------------------------------

    if save_history:

        _save_bill_history(bill)

    return {
        "a4": a4_path,
        "80mm": thermal_path,
        "bill": bill,
    }
