#!/usr/bin/env python

import os
import sys
from datetime import datetime

from malcheck_client.gui import message_box
from malcheck_client.file import files_task
from malcheck_client.addons import addons_task
from malcheck_client.process import process_task
from malcheck_client.network import network_task
from malcheck_client.powershell import pwsh_task
from malcheck_client.sysinfo import sysinfo_task
from malcheck_client.autorun import autorun_task
from malcheck_client.activity import activity_task
from malcheck_client.utils import is_admin, zip_list_file
from malcheck_client.utils import internet_check_by_requests
# from malcheck_client.storage import storage_task

# from malcheck_client.storage import object_upload
# from malcheck_client.config import BUCKETS_NAME


def main():
    if not is_admin():
        message_box("Oops!", "This program requires run as Administrator", 0)
        sys.exit(1)

    if not internet_check_by_requests():
        message_box("Oops!", "Please check your internet connection", 0)
        sys.exit(2)

    sysinfo_data = sysinfo_task()
    activity_data = activity_task()
    addons_data = addons_task()
    autorun_data = autorun_task()
    powershell_data = pwsh_task()
    file_data = files_task()
    network_data = network_task()
    process_data = process_task()
    obj_path = zip_list_file()
    # Debug
    print(obj_path)

    # Get pre-signed URL string to upload object
    # upload_result = storage_task()
    # timestamp = datetime.today()
    # location = f"{timestamp.year}/{timestamp.month}/{os.path.basename(obj_path)}"
    # if object_upload(location, obj_path):
    #     print("Successful upload report!")


if __name__ == "__main__":
    main()
