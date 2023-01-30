from malcheck_utils.config import PACKAGE_DIR
from malcheck_utils.config import NIRSOFT_ZIP, NIRSOFT_URL
from malcheck_utils.config import SYSINTERNAL_BIN, SYSINTERNAL_URL

import os
import time
import shutil
import requests
import platform


def download_file_from_url(url, dst_dir):
    try:
        local_filename = os.path.join(dst_dir, url.split('/')[-1])
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        return os.path.basename(local_filename)
    except Exception as ex:
        print(ex)


# Update Task: Download latest version of binaries dependencies
def malcheck_update():
    try:
        print("[UPDATE] Updating binaries dependencies")
        if not os.path.exists(PACKAGE_DIR):
            os.mkdir(PACKAGE_DIR)
        os_platform = platform.system()
        if os_platform.lower() == "windows":
            print(f"[UPDATE] Platform detected: {os_platform}")
            packs = os.listdir(PACKAGE_DIR)
            missing_file = []
            total_files = SYSINTERNAL_BIN + NIRSOFT_ZIP
            for bin_ in total_files:
                if bin_ not in packs:
                    missing_file.append(bin_)
            if len(missing_file) > 0:
                print(f"[UPDATE] Missing {len(missing_file)} file: {missing_file}")
            file_downloaded = []
            print("[UPDATE] Download missing binaries dependencies")
            for file_ in missing_file:
                if file_ in SYSINTERNAL_BIN:
                    url = SYSINTERNAL_URL + file_
                    file_downloaded.append(download_file_from_url(url, PACKAGE_DIR))
                elif file_ in NIRSOFT_ZIP:
                    url = NIRSOFT_URL + file_
                    file_downloaded.append(download_file_from_url(url, PACKAGE_DIR))
            if len(file_downloaded) > 0:
                print(f"[UPDATE] Total {len(file_downloaded)} file downloaded: {file_downloaded}")
            print("[UPDATE] Done!\n")
        time.sleep(0.5)
    except Exception as ex:
        print(ex)
