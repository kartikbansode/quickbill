import json
import os
import datetime

from logic.file_paths import data_path

HOLD_FILE = data_path("held_bills.json")


def load_held_bills():

    if not os.path.exists(HOLD_FILE):
        return []

    try:

        with open(HOLD_FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    except:

        return []


def save_held_bills(bills):

    with open(HOLD_FILE, "w", encoding="utf-8") as f:

        json.dump(bills, f, indent=4)


def hold_bill(cart):

    bills = load_held_bills()

    next_no = 1

    if bills:

        numbers = [
            int(b["hold_no"].split("-")[1])
            for b in bills
        ]

        next_no = max(numbers) + 1

    hold_no = f"HB-{next_no:06d}"

    bills.append(
        {
            "hold_no": hold_no,
            "date": datetime.datetime.now().strftime("%d-%m-%Y"),
            "time": datetime.datetime.now().strftime("%I:%M %p"),
            "cart": cart,
        }
    )

    save_held_bills(bills)

    return hold_no


def delete_hold_bill(hold_no):

    bills = load_held_bills()

    bills = [b for b in bills if b["hold_no"] != hold_no]

    save_held_bills(bills)


def get_all_hold_bills():

    return load_held_bills()