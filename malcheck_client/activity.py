import os
import csv
import time
import platform
import subprocess

from malcheck_client.logging import logger
from malcheck_client.crypto import string_random
from malcheck_client.utils import write_dicts_to_json_file
from malcheck_client.config import DATA_DIR, NIRSOFT_LASTACTIVITYVIEW

WIN_ACTIVITY_FIELD = ["time", "action", "name", "path", "information", "extension", "source"]
WIN_ACTIVITY_FILTER = ["Run .EXE file", "Software Installation", "Task Run"]


def activity_csv_to_dicts(csv_file):
    try:
        data = list()
        temp = list()
        reader = csv.DictReader(open(csv_file))
        # reader.fieldnames = [x.replace(" ", "_").lower() for x in reader.fieldnames]
        reader.fieldnames = WIN_ACTIVITY_FIELD
        for row in reader:
            temp.append(row)
        # Filter event
        for item in temp:
            if item["action"] in WIN_ACTIVITY_FILTER:
                data.append(item)
    except Exception as ex:
        logger.info(str(ex))
    else:
        return data


def activity_scan_on_windows():
    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        csv_file = os.path.join(DATA_DIR, ".".join([string_random(6), "tmp"]))
        lastactivityview_cmd = [NIRSOFT_LASTACTIVITYVIEW, "/scomma", csv_file]
        lastactivityview_output = subprocess.run(lastactivityview_cmd, stdout=subprocess.PIPE, shell=True)
        time.sleep(1)
    except Exception as ex:
        logger.info(str(ex))
    else:
        return csv_file


def get_activity_windows():
    try:
        data = list()
        activity_csv = activity_scan_on_windows()
        if os.path.exists(activity_csv):
            data = activity_csv_to_dicts(activity_csv)
    except Exception as ex:
        logger.info(str(ex))
    else:
        return data


# Last Activity on system (Windows)
def activity_task():
    logger.info("Starting activity task")
    activity_data = list()
    os_platform = platform.system()
    if os_platform == "Windows":
        activity_data = get_activity_windows()
    elif os_platform == "Linux":
        pass
    elif os_platform == "Darwin":
        pass
    else:
        return activity_data.append("Operating system is not detected.")
    write_dicts_to_json_file(activity_data, "activity.json")
    return len(activity_data)
