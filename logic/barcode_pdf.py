from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from logic.resource_path import resource_path

from logic.file_paths import app_path

BARCODE_FOLDER = app_path("barcodes")


pdfmetrics.registerFont(
    TTFont(
        "DejaVu",
        resource_path("assets/fonts/DejaVuSans.ttf"),
    )
)

pdfmetrics.registerFont(
    TTFont(
        "DejaVu-Bold",
        resource_path("assets/fonts/DejaVuSans-Bold.ttf"),
    )
)


class BarcodeLayout:

    def __init__(
        self,
        columns=2,
        rows=5,
    ):

        self.page_width = 210 * mm
        self.page_height = 297 * mm

        self.columns = columns
        self.rows = rows

        self.margin_left = 6 * mm
        self.margin_right = 6 * mm

        self.margin_top = 8 * mm
        self.margin_bottom = 8 * mm

        self.gap_x = 3 * mm
        self.gap_y = 4 * mm

        self.calculate()

    def calculate(self):

        printable_width = self.page_width - self.margin_left - self.margin_right

        printable_height = self.page_height - self.margin_top - self.margin_bottom

        self.label_width = (
            printable_width - ((self.columns - 1) * self.gap_x)
        ) / self.columns

        calculated_height = (
            printable_height - ((self.rows - 1) * self.gap_y)
        ) / self.rows

        self.label_height = max(
            calculated_height,
            46 * mm,
        )

    def position(self, index):

        col = index % self.columns

        row = (index // self.columns) % self.rows

        page = index // (self.columns * self.rows)

        x = self.margin_left + (col * (self.label_width + self.gap_x))

        y = (
            self.page_height
            - self.margin_top
            - self.label_height
            - row * (self.label_height + self.gap_y)
        )

        return page, x, y


from reportlab.graphics.barcode.code128 import Code128
from reportlab.pdfgen import canvas

import os


class BarcodeLabel:

    def __init__(self, canvas, x, y, width, height):

        self.canvas = canvas

        self.x = x
        self.y = y

        self.width = width
        self.height = height

    def draw(
        self,
        barcode,
        name,
        price,
        show_name=True,
        show_price=True,
        show_number=True,
    ):

        self.canvas.setLineWidth(0.4)
        self.canvas.setStrokeColorRGB(0.55, 0.55, 0.55)

        self.canvas.roundRect(
            self.x,
            self.y,
            self.width,
            self.height,
            2,
            stroke=1,
            fill=0,
        )

        center_x = self.x + self.width / 2

        # -----------------------------
        # Layout
        # -----------------------------

        padding_top = 5 * mm
        padding_bottom = 5 * mm

        barcode_height = 26 * mm

        line_gap = 2.5 * mm

        content_height = barcode_height

        if show_number:
            content_height += 4 * mm + line_gap

        if show_name:
            content_height += 5 * mm + line_gap

        if show_price:
            content_height += 6 * mm

        # Start drawing from top of label
        current_y = self.y + self.height - padding_top
        # -------------------------
        # Barcode
        # -------------------------

        barcode_obj = Code128(
            barcode,
            barWidth=0.65 * mm,
            barHeight=26 * mm,
            humanReadable=False,
        )

        barcode_width = barcode_obj.width

        barcode_x = self.x + (self.width - barcode_width) / 2

        barcode_y = current_y - barcode_height

        barcode_obj.drawOn(
            self.canvas,
            barcode_x,
            barcode_y,
        )

        current_y = barcode_y - 7 * mm

        # -------------------------
        # Barcode Number
        # -------------------------

        if show_number:

            self.canvas.setFont(
                "DejaVu",
                11,
            )

            self.canvas.drawCentredString(
                center_x,
                current_y,
                barcode,
            )

            current_y -= 4 * mm + line_gap
        # -------------------------
        # Product Name
        # -------------------------

        if show_name:

            self.canvas.setFont(
                "DejaVu-Bold",
                9,
            )

            text = name

            if len(text) > 28:
                text = text[:25] + "..."

            self.canvas.drawCentredString(
                center_x,
                current_y,
                text,
            )

            current_y -= 6 * mm + line_gap
        # -------------------------
        # Price
        # -------------------------

        if show_price:

            self.canvas.setFont(
                "DejaVu-Bold",
                11,
            )

            self.canvas.drawCentredString(
                center_x,
                current_y,
                f"MRP ₹ {price:.2f}",
            )


def generate_barcode_pdf(
    products,
    show_name=True,
    show_price=True,
    show_number=True,
    columns=2,
    rows=5,
):

    os.makedirs(
        BARCODE_FOLDER,
        exist_ok=True,
    )

    pdf_path = os.path.join(
        BARCODE_FOLDER,
        "barcode_labels.pdf",
    )

    pdf = canvas.Canvas(pdf_path)

    layout = BarcodeLayout(
        columns=columns,
        rows=rows,
    )

    current_page = 0

    for index, product in enumerate(products):

        page, x, y = layout.position(index)

        if page != current_page:

            pdf.showPage()

            current_page = page

        label = BarcodeLabel(
            pdf,
            x,
            y,
            layout.label_width,
            layout.label_height,
        )

        label.draw(
            barcode=str(product["barcode"]),
            name=product["name"],
            price=float(product["selling_price"]),
            show_name=show_name,
            show_price=show_price,
            show_number=show_number,
        )

    pdf.save()

    return pdf_path
