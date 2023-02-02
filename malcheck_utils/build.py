from malcheck_utils.config import RELEASE_DIR, PACKER_DIR, BASE_DIR
from malcheck_utils.config import PY_LAUNCHER_NAME, EXE_LAUNCHER_NAME

import os
import time
import random
import string
import platform
import PyInstaller.__main__


def string_random(n):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(n))


def malcheck_build():
    try:
        print("[BUILD] Building MalCheck client")
        os_platform = platform.system().lower()
        tiny_aes_key = string_random(16)
        release_path = os.path.join(RELEASE_DIR, os_platform)
        icon_path = os.path.join(BASE_DIR, "assets", "icon.ico")
        if os_platform == 'windows':
            upx_packer = os.path.join(PACKER_DIR, 'upx_win64')
            PyInstaller.__main__.run(
                ['--clean', '--uac-admin', '--icon', icon_path, '--onefile', '--noconsole', '--name', EXE_LAUNCHER_NAME, '--add-data',
                 'bins;bins', '--add-data', 'keys;keys',
                 '--distpath', release_path, '--upx-dir', upx_packer, '--key', tiny_aes_key, PY_LAUNCHER_NAME])
        elif os_platform == 'linux':
            pass
        elif os_platform == 'macosx':
            pass
        else:
            print("[BUILD] Platform does not support!\n")
        time.sleep(0.5)
    except Exception as ex:
        print(ex)
