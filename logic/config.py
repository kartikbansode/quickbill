import json
import os

from logic.resource_path import resource_path

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "company": {
        "name": "QuickBill Systems",
        "owner": "Admin",
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
        "camera_url": "http://192.168.0.133:8080/video",
        "duplicate_delay": 1,
        "beep": True
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
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def get(section, key):
    return config[section][key]


def set(section, key, value):
    config[section][key] = value
    save_config()