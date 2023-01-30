import os

TEMP = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(TEMP)
BINS_DIR = os.path.join(BASE_DIR, "bins")
DATA_DIR = os.path.join(BASE_DIR, "data")
KEYS_DIR = os.path.join(BASE_DIR, "keys")
BUILD_DIR = os.path.join(BASE_DIR, 'build')
PACKER_DIR = os.path.join(BASE_DIR, 'packer')
RSA_KEY_DIR = os.path.join(BASE_DIR, 'rsa_keys')
PACKAGE_DIR = os.path.join(BASE_DIR, 'packages')
RELEASE_DIR = os.path.join(BASE_DIR, 'releases')

SYSINTERNAL_URL = "https://live.sysinternals.com/"
NIRSOFT_URL = "https://www.nirsoft.net/utils/"
SYSINTERNAL_BIN = ["autorunsc.exe", "sigcheck.exe"]
NIRSOFT_ZIP = ["browseraddonsview.zip", "cports.zip", "lastactivityview.zip"]
GEOIP_ZIP = ["GeoLite2-Country.zip"]
RSA_PUB_KEY = "malcheck.pub"
RSA_PRI_KEY = "malcheck.pri"
PY_LAUNCHER_NAME = "malcheck_client.py"
EXE_LAUNCHER_NAME = "malcheck_client"
