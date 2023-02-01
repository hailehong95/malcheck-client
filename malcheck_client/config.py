import os

TEMP = os.path.dirname(os.path.abspath(__file__))
CWD_DIR = os.getcwd()
BASE_DIR = os.path.dirname(TEMP)
BINS_DIR = os.path.join(BASE_DIR, "bins")
DATA_DIR = os.path.join(BASE_DIR, "data")
KEYS_DIR = os.path.join(BASE_DIR, "keys")

SYSINTERNAL_AUTORUN = os.path.join(BINS_DIR, "autorunsc.exe")
SYSINTERNAL_SIGCHECK = os.path.join(BINS_DIR, "sigcheck.exe")
NIRSOFT_LASTACTIVITYVIEW = os.path.join(BINS_DIR, "LastActivityView.exe")
NIRSOFT_BROWSERADDONSVIEW = os.path.join(BINS_DIR, "BrowserAddonsView.exe")
GEOLITE2_DB = os.path.join(BINS_DIR, "GeoLite2-Country.mmdb")
NIRSOFT_CPORTS = os.path.join(BINS_DIR, "cports.exe")
LOG_PATH = os.path.join(CWD_DIR, "malcheck-client.log")
STORAGE_BASE_URL = "storage.example.demo"
MAX_SIZE_FILE = 12 * 1024 * 1024  # 12MB
BUCKETS_NAME = "YOUR-BUCKET-NAME"
