import os
import csv
import time
import platform
import subprocess

from malcheck_client.logging import logger
from malcheck_client.crypto import string_random
from malcheck_client.utils import write_dicts_to_json_file
from malcheck_client.config import DATA_DIR, SYSINTERNAL_AUTORUN


def autorun_csv_to_dicts(csv_file):
    try:
        data = list()
        temp = list()
        reader = csv.DictReader(open(csv_file))
        reader.fieldnames = [x.replace(" ", "_").replace("-", "").lower() for x in reader.fieldnames]
        for row in reader:
            if row["sha1"]:
                temp.append(row)
        # Sanitize fields
        for item in temp:
            tmp = {
                "time": item["time"],
                "location": item["entry_location"],
                "name": item["entry"],
                "status": item["enabled"],
                "category": item["category"],
                "description": item["description"] if item["description"] else "unknown",
                "verified": item["signer"] if item["signer"] else "unknown",
                "company": item["company"] if item["company"] else "unknown",
                "path": item["image_path"],
                "version": item["version"] if item["version"] else "unknown",
                "cmdline": item["launch_string"],
                "md5": item["md5"],
                "sha1": item["sha1"],
                "sha256": item["sha256"]
            }
            data.append(tmp)
    except Exception as ex:
        logger.info(str(ex))
    else:
        return data


# Scanning autoruns key on Windows
def autorun_scan_on_windows():
    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        autorun_csv = os.path.join(DATA_DIR, ".".join([string_random(6), "tmp"]))
        autorun_cmd = [SYSINTERNAL_AUTORUN, "-accepteula", "-nobanner", "-a", "*", "-c", "-h", "-s", "-m", "-o", autorun_csv]
        autorun_output = subprocess.run(autorun_cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(1)
    except Exception as ex:
        autorun_csv = ""
        logger.info(str(ex))
    else:
        return autorun_csv


# Autoruns keys on Windows
def get_autorun_windows():
    try:
        data = list()
        autorun_csv = autorun_scan_on_windows()
        if os.path.exists(autorun_csv):
            data = autorun_csv_to_dicts(autorun_csv)
    except Exception as ex:
        logger.info(str(ex))
    else:
        return data


# Get Autoruns key: bootstart, persistent, autostart program
def autorun_task():
    logger.info("Starting autorun task")
    autorun_data = list()
    os_platform = platform.system()
    if os_platform == "Windows":
        autorun_data = get_autorun_windows()
    elif os_platform == "Linux":
        pass
    elif os_platform == "Darwin":
        pass
    else:
        return autorun_data.append("Operating system is not detected.")
    write_dicts_to_json_file(autorun_data, "autorun.json")
    return len(autorun_data)
