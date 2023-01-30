import os
import time
import platform
import subprocess

from malcheck_client.config import DATA_DIR
from malcheck_client.crypto import string_random
from malcheck_client.utils import write_dicts_to_json_file


def dump_pwsh_events_windows():
    try:
        if not os.path.isdir(DATA_DIR):
            os.mkdir(DATA_DIR)
        wevtutil_bin = "wevtutil.exe"
        txt_file = os.path.join(DATA_DIR, '.'.join([string_random(6), 'tmp']))
        wevtutil_cmd = wevtutil_bin + ' qe "Windows Powershell" /rd:true /f:text /uni:true > ' + txt_file
        wevtutil_output = subprocess.check_output(wevtutil_cmd, stderr=open(os.devnull, 'w'), shell=True)
        time.sleep(1)
    except Exception as ex:
        print(ex)
    else:
        return txt_file


def get_index_of_item(word, dct):
    for item in dct:
        if word in item:
            return dct.index(item)
    return -1


def pwsh_txt_to_dicts(txt_file):
    try:
        pwsh_list = list()
        with open(txt_file, 'r', encoding='utf-16') as fin:
            raw_data = fin.read()
        temp_events = raw_data.split('CommandLine=\n\n')
        if not temp_events[-1]:
            temp_events.pop()
        common_field = {'log_name': 'Log Name:', 'date': 'Date:', 'event_id': 'Event ID:', 'task': 'Task:',
                        'level': 'Level:', 'username': 'User Name:', 'computer': 'Computer:',
                        'description': 'Description:'}
        details_field = {'host_name': 'HostName=', 'host_version': 'HostVersion=',
                         'host_id': 'HostId=', 'host_application': 'HostApplication='}
        for temp in temp_events:
            pwsh_dict = dict()
            details = dict()
            event = [x.strip() for x in temp.replace('\t', '').splitlines() if x.strip()]
            for key, val in common_field.items():
                if key == "description":
                    pwsh_dict[key] = event[get_index_of_item(val, event) + 1].strip()
                else:
                    pwsh_dict[key] = event[get_index_of_item(val, event)].split(val)[-1].strip()
            for key, val in details_field.items():
                details[key] = event[get_index_of_item(val, event)].split(val)[-1].strip()
            pwsh_dict["details"] = details
            pwsh_list.append(pwsh_dict)
        time.sleep(1)
    except Exception as ex:
        print(ex)
    else:
        return pwsh_list


def get_pwsh_logs_windows():
    pwsh_list = list()
    try:
        txt_file = dump_pwsh_events_windows()
        pwsh_list = pwsh_txt_to_dicts(txt_file)
    except Exception as ex:
        print(ex)
    return pwsh_list


# Get powershell event/log on system
def pwsh_task():
    pwsh_data = list()
    os_platform = platform.system()
    if os_platform == "Windows":
        pwsh_data = get_pwsh_logs_windows()
    elif os_platform == "Linux":
        pass
    elif os_platform == "Darwin":
        pass
    else:
        return pwsh_data.append("Operating system is not detected.")
    write_dicts_to_json_file(pwsh_data, "powershell.json")
    return len(pwsh_data)
