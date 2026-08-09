from io import BytesIO
from urllib.parse import quote

import qrcode
from PIL import ImageTk


DEFAULT_UPI_ID = "8793432136-5@ybl"
DEFAULT_MERCHANT_NAME = "QuickBill"


def build_upi_payload(
    upi_id,
    amount,
    bill_no,
    merchant_name=DEFAULT_MERCHANT_NAME,
):
    upi_id = str(upi_id or "").strip()
    merchant_name = str(merchant_name or DEFAULT_MERCHANT_NAME).strip()
    bill_no = str(bill_no or "").strip()

    if not upi_id:
        raise ValueError("UPI ID is required.")

    amount = round(float(amount), 2)

    if amount <= 0:
        raise ValueError("UPI amount must be greater than zero.")

    params = [
        f"pa={quote(upi_id, safe='')}",
        f"pn={quote(merchant_name, safe='')}",
        f"am={amount:.2f}",
        "cu=INR",
    ]

    if bill_no:
        params.append(f"tr={quote(bill_no, safe='')}")
        params.append(
            f"tn={quote(f'QuickBill-{bill_no}', safe='')}"
        )

    return "upi://pay?" + "&".join(params)


def create_upi_qr_image(
    upi_id,
    amount,
    bill_no,
    merchant_name=DEFAULT_MERCHANT_NAME,
    size=250,
):
    payload = build_upi_payload(
        upi_id=upi_id,
        amount=amount,
        bill_no=bill_no,
        merchant_name=merchant_name,
    )

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    ).convert("RGB")

    image = image.resize((int(size), int(size)))

    return image, payload


def create_upi_qr_photoimage(
    master,
    upi_id,
    amount,
    bill_no,
    merchant_name=DEFAULT_MERCHANT_NAME,
    size=250,
):
    image, payload = create_upi_qr_image(
        upi_id=upi_id,
        amount=amount,
        bill_no=bill_no,
        merchant_name=merchant_name,
        size=size,
    )

    return ImageTk.PhotoImage(image=image, master=master), payload