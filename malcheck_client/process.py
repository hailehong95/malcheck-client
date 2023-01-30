import os
import psutil
import platform

from malcheck_client.config import DATA_DIR
from malcheck_client.utils import pe_signature_check, get_hash_file
from malcheck_client.utils import write_dicts_to_json_file


# Process running on Windows, Linux, macOS
def get_process_running():
    try:
        data = list()
        os_platform = platform.system()
        attrs = ["pid", "name", "status", "create_time", "username", "exe", "cmdline"]
        procs = psutil.process_iter(attrs, ad_value=None)
        for x in procs:
            x.info["cmdline"] = " ".join(x.info["cmdline"]) if x.info["cmdline"] else "unknown"
            if x.info["exe"] and os.path.exists(x.info["exe"]):
                hash_data = get_hash_file(x.info["exe"])
                x.info["md5"] = hash_data.get("md5")
                x.info["sha1"] = hash_data.get("sha1")
                x.info["sha256"] = hash_data.get("sha256")
                if os_platform == "Windows":
                    verified_data = pe_signature_check(x.info["exe"])
                    x.info["verified"] = verified_data.get("verified")
                    x.info["signing_date"] = verified_data.get("signing_date")
                    x.info["publisher"] = verified_data.get("publisher")
                    x.info["machine_type"] = verified_data.get("machine_type")
            else:
                x.info["exe"] = "unknown"
                x.info["hash"] = "unknown"
                x.info["verified"] = "unknown"
            data.append(x.info)
        # replace "exe" with "path"
        for item in data:
            item["path"] = item.pop("exe")
    except Exception as ex:
        print(ex)
    else:
        return data


# Get Process running on system
def process_task():
    process_data = list()
    if platform.system() in ["Windows", "Linux", "Darwin"]:
        process_data = get_process_running()
    else:
        process_data.append("Operating system is not detected.")
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    write_dicts_to_json_file(process_data, "process.json")
    return len(process_data)
