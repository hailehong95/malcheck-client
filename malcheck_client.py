#!/usr/bin/env python

import sys

from malcheck_client.gui import main_gui
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
from malcheck_client.storage import get_pre_signed_url, pre_signed_upload


def main():
    if not is_admin():
        message_box("Oops!", "This program requires run as Administrator", 0)
        sys.exit(1)

    if not internet_check_by_requests():
        message_box("Oops!", "Please check your internet connection", 0)
        sys.exit(2)

    # main_gui()

    sysinfo_data = sysinfo_task()
    activity_data = activity_task()
    addons_data = addons_task()
    autorun_data = autorun_task()
    powershell_data = pwsh_task()
    file_data = files_task()
    network_data = network_task()
    process_data = process_task()
    obj_path = zip_list_file()
    pre_signed_url = get_pre_signed_url("100123_NguyenVanAn_20230209222647.zip")
    if pre_signed_url is None:
        message_box("Oops!", "Failed get pre-signed url!", 0)
        sys.exit(3)
    upload_result = pre_signed_upload(pre_signed_url, obj_path)
    if upload_result:
        message_box("Oops!", "Successful upload report!", 0)
    else:
        message_box("Oops!", "Failed upload report!", 0)


if __name__ == "__main__":
    main()
