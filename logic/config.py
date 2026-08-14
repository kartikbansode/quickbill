import json
import os

from logic.resource_path import resource_path

from logic.file_paths import data_path

CONFIG_FILE = data_path("config.json")

DEFAULT_CONFIG = {
    "company": {
        "cashier_name": "Admin",
        "name": "QuickBill Pro",
        "address": "",
        "phone": "",
        "email": "",
        "gst": "",
        "logo": resource_path("assets/images/logo.png")
    },

    "billing": {
        "currency": "₹",
        "invoice_prefix": "QB",
        "tax_percent": 10,
        "discount_percent": 5,
        "round_off": True
    },

    "scanner": {
        "type": "mobile_camera",
        "camera_url": "",
        "duplicate_delay": 1,
        "beep": True
    },

    "payment": {
        "upi_id": ""
    }
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


config = load_config()


def save_config():
    temp_file = CONFIG_FILE + ".tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        os.replace(temp_file, CONFIG_FILE)
    except Exception as e:
        print(f"[ERROR] Failed to save config: {e}")
        try:
            os.remove(temp_file)
        except OSError:
            pass


def get(section, key, default=None):
    return config.get(section, {}).get(key, default)


def set(section, key, value):
    if section not in config:
        config[section] = {}
    config[section][key] = value
    save_config()


def get_currency():
    return config.get("billing", {}).get("currency", "₹")


def get_invoice_prefix():
    return config.get("billing", {}).get("invoice_prefix", "INV")


def get_tax_percent():
    try:
        return float(config.get("billing", {}).get("tax_percent", 10))
    except (ValueError, TypeError):
        return 10.0


def get_discount_percent():
    try:
        return float(config.get("billing", {}).get("discount_percent", 5))
    except (ValueError, TypeError):
        return 5.0


def get_round_off():
    return bool(config.get("billing", {}).get("round_off", True))