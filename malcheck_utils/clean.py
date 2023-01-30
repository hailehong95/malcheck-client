from malcheck_utils.config import RELEASE_DIR, BUILD_DIR
from malcheck_utils.config import BINS_DIR, DATA_DIR, KEYS_DIR

import os
import time
import shutil


# Clean Task: Remove all binaries dependencies in some directory
def malcheck_clean():
    try:
        print("[CLEAN] Remove temporary working files")
        dirs_delete = [BINS_DIR, KEYS_DIR, DATA_DIR, RELEASE_DIR, BUILD_DIR]
        for path in dirs_delete:
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
                time.sleep(0.5)
        print("[CLEAN] Done!\n")
    except Exception as ex:
        print(ex)
