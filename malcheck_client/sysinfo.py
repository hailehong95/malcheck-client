import os
import shlex
import socket
import psutil
import distro
import getpass
import platform
import subprocess
from datetime import datetime

from malcheck_client.logging import logger
from malcheck_client.config import DATA_DIR
from malcheck_client.utils import write_dicts_to_json_file
from malcheck_client.utils import internet_check_by_requests
from malcheck_client.utils import get_primary_ip_with_internet
from malcheck_client.utils import get_primary_ip_without_internet


def get_network_info():
    network_info = list()
    primary_ip = [get_primary_ip_with_internet(), get_primary_ip_without_internet()]
    primary_ip = list(set(primary_ip))
    for interface, snicaddrs in psutil.net_if_addrs().items():
        if len(snicaddrs) > 2:
            temp = dict()
            temp["interface"] = interface
            for snic in snicaddrs:
                if snic.family == socket.AF_INET:
                    temp["ipv4"] = snic.address
                    temp["internet_on"] = True if snic.address in primary_ip else False
                elif snic.family == socket.AF_INET6:
                    temp["ipv6"] = snic.address
                else:
                    temp["mac_address"] = snic.address
            network_info.append(temp)
    return network_info


def get_primary_network():
    net_data = dict()
    network_info = list()
    if internet_check_by_requests():
        primary_ip = get_primary_ip_with_internet()
    else:
        primary_ip = get_primary_ip_without_internet()
    for interface, snicaddrs in psutil.net_if_addrs().items():
        for snic in snicaddrs:
            if snic.address == primary_ip:
                network_info = psutil.net_if_addrs()[interface]
                net_data["interface"] = interface
    net_data["ipv4"] = [x.address for x in network_info if x.family == socket.AF_INET][0]
    # net_data["ipv6"] = [x.address for x in network_info if x.family == socket.AF_INET6][0]
    net_data["mac_address"] = [x.address for x in network_info if x.family != socket.AF_INET6 and x.family != socket.AF_INET][0]
    return net_data


# Get all information in Windows, Linux, macOS
def get_system_info():
    data = list()
    temp = dict()
    os_platform = platform.system()
    try:
        temp["os"] = os_platform
        temp["type"] = platform.machine()
        if os_platform == "Windows":
            temp["version"] = " ".join([platform.system(), platform.release(), platform.win32_edition()])
            temp["build"] = platform.version()
        else:
            temp["version"] = " ".join(distro.linux_distribution())
            temp["build"] = platform.release()
        temp["hostname"] = platform.node()
        temp["username"] = getpass.getuser()
        temp["boot_time"] = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        temp["network"] = get_network_info()
        # temp["primary_network"] = get_primary_network()
        if os_platform == "Windows":
            wmic_cmd = "wmic qfe get hotfixid"
            hotfix_output = subprocess.run(shlex.split(wmic_cmd), stdout=subprocess.PIPE, shell=True)
            hotfix_output = hotfix_output.stdout.decode("utf-8", errors="ignore").replace("\r\r\n", "").split(" ")
            hotfix = [x for x in hotfix_output if x != "HotFixID" and x != ""]
            hotfix.sort()
            temp["hotfix"] = hotfix
        data.append(temp)
    except Exception as ex:
        logger.info(str(ex))
    return data


# Get information on system
def sysinfo_task():
    logger.info("Starting sysinfo task")
    system_info = list()
    if platform.system() in ["Windows", "Linux", "Darwin"]:
        system_info = get_system_info()
    else:
        system_info.append("Operating system is not detected.")
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    write_dicts_to_json_file(system_info, "sysinfo.json")
    return len(system_info)
