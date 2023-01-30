import os
import csv
import time
import platform
import subprocess

from malcheck_client.crypto import string_random
from malcheck_client.utils import write_dicts_to_json_file
from malcheck_client.config import DATA_DIR, NIRSOFT_BROWSERADDONSVIEW

WIN_ADDON_COLUMNS = "Item ID,Status,Web Browser,Addon Type,Name,Version,Description,Install Time"
WIN_ADDON_FIELD = ["id", "status", "browser", "type", "name", "version", "description", "install_time"]


def addon_csv_to_dicts(csv_file):
    try:
        data = list()
        temp = list()
        reader = csv.DictReader(open(csv_file))
        # reader.fieldnames = [x.replace(" ", "_").lower() for x in reader.fieldnames]
        reader.fieldnames = WIN_ADDON_FIELD
        for row in reader:
            temp.append(row)
        # Filter event
        for item in temp:
            if item["name"]:
                if item["id"].find(" ") == -1:
                    data.append(item)
    except Exception as ex:
        print(ex)
    else:
        return data


def addon_scan_on_windows():
    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        csv_file = os.path.join(DATA_DIR, ".".join([string_random(6), "tmp"]))
        browseraddonsview_cmd = [NIRSOFT_BROWSERADDONSVIEW, "/scomma", csv_file, "/Columns", WIN_ADDON_COLUMNS]
        browseraddonsview_output = subprocess.run(browseraddonsview_cmd, stdout=subprocess.PIPE)
        time.sleep(1)
    except Exception as ex:
        print(ex)
    else:
        return csv_file


def get_addon_windows():
    try:
        data = list()
        addon_csv = addon_scan_on_windows()
        if os.path.exists(addon_csv):
            data = addon_csv_to_dicts(addon_csv)
    except Exception as ex:
        print(ex)
    else:
        return data


# Get Browser add-on on system
def addons_task():
    addon_data = list()
    os_platform = platform.system()
    if os_platform == "Windows":
        addon_data = get_addon_windows()
    elif os_platform == "Linux":
        pass
    elif os_platform == "Darwin":
        pass
    else:
        return addon_data.append("Operating system is not detected.")
    write_dicts_to_json_file(addon_data, "addon.json")
    return len(addon_data)
