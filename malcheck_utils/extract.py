from malcheck_utils.config import BINS_DIR, PACKAGE_DIR
from malcheck_utils.config import SYSINTERNAL_BIN, NIRSOFT_ZIP, GEOIP_ZIP

import os
import time
import shutil
import zipfile
import platform


def unzip_file(zip_file, dst_dir):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(dst_dir)
    except Exception as ex:
        print(ex)


# Extract Task: unzip and copy binaries dependencies to 'bin' directory.
def malcheck_extract():
    try:
        print("[EXTRACT] Extracting MalCheck client")
        if not os.path.isdir(BINS_DIR):
            os.mkdir(BINS_DIR)
        os_platform = platform.system()
        if os_platform.lower() == "windows":
            print(f"[EXTRACT] Platform detected: {os_platform}")
            print(f"[EXTRACT] Copy SysInternal file: {SYSINTERNAL_BIN}")
            for _exe in SYSINTERNAL_BIN:
                shutil.copyfile(os.path.join(PACKAGE_DIR, _exe), os.path.join(BINS_DIR, _exe))
                time.sleep(0.5)
            print(f"[EXTRACT] Extract Zip and copy NirSoft file: {NIRSOFT_ZIP}")
            for _zip in NIRSOFT_ZIP:
                unzip_file(os.path.join(PACKAGE_DIR, _zip), BINS_DIR)
                time.sleep(0.5)
            print(f"[EXTRACT] Extract and copy GeoLite2-Country file: {GEOIP_ZIP}")
            for _zip in GEOIP_ZIP:
                unzip_file(os.path.join(PACKAGE_DIR, _zip), BINS_DIR)
                time.sleep(0.5)
            extensions = {".txt", ".chm"}
            files = os.listdir(BINS_DIR)
            files_removed = []
            for file_ in files:
                for ext in extensions:
                    if file_.endswith(ext):
                        files_removed.append(file_)
                        os.remove(os.path.join(BINS_DIR, file_))
                        time.sleep(0.5)
            print(f"[EXTRACT] Removed {len(files_removed)} optional files: {files_removed}")
            print("[EXTRACT] Done!\n")
    except Exception as ex:
        print(ex)
