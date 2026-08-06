import json
import os

from logic.file_paths import data_path

BILLS_FILE = data_path("bills_history.json")


def get_all_bills():

    if not os.path.exists(BILLS_FILE):

        return []

    try:

        with open(BILLS_FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    except:

        return []


def search_bill_history(keyword):

    keyword = keyword.lower().strip()

    bills = get_all_bills()

    if not keyword:

        return bills

    results = []

    for bill in bills:

        if (
            keyword in bill.get("bill_no", "").lower()
            or keyword in bill.get("payment_mode", "").lower()
            or keyword in bill.get("date", "").lower()
        ):

            results.append(bill)

    return results