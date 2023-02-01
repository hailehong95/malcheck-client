import os
import socket
import psutil
import platform

from malcheck_client.logging import logger
from malcheck_client.config import DATA_DIR, GEOLITE2_DB
from malcheck_client.utils import write_dicts_to_json_file, geoip_country


# Network connection on Windows, Linux, macOS
def get_network_connection():
    proto_map = {
        (socket.AF_INET, socket.SOCK_STREAM): "tcp",
        (socket.AF_INET6, socket.SOCK_STREAM): "tcp6",
        (socket.AF_INET, socket.SOCK_DGRAM): "udp",
        (socket.AF_INET6, socket.SOCK_DGRAM): "udp6",
    }
    try:
        conn = list()
        procs_data = list()
        remote_ips = list()
        attrs = ["pid", "name", "exe"]
        procs_temp = psutil.process_iter(attrs, ad_value=None)
        nets_temp = psutil.net_connections(kind="inet")

        for it in procs_temp:
            procs_data.append(it.info)
        for c in nets_temp:
            data = dict()
            data["protocol"] = proto_map[(c.family, c.type)]
            data["local_address"] = c.laddr.ip
            data["local_port"] = c.laddr.port
            data["remote_address"] = c.raddr.ip if c.raddr else "unknown"
            data["remote_port"] = c.raddr.port if c.raddr else "unknown"
            data["status"] = c.status
            data["pid"] = c.pid or "unknown"
            data["name"] = "unknown"
            data["path"] = "unknown"
            if data["pid"] != "unknown":
                for item in procs_data:
                    if item.get("pid") == data.get("pid"):
                        data["name"] = item.get("name")
                        data["path"] = item.get("exe")
            conn.append(data)
            remote_ips.append(data["remote_address"])
        # geoip country
        remote_ips = list(set(remote_ips))
        ips_country = geoip_country(GEOLITE2_DB, remote_ips)
        conn_data = list()
        for item in conn:
            item["country"] = ips_country.get(item.get("remote_address"))
            conn_data.append(item)
    except Exception as ex:
        logger.info(str(ex))
    else:
        return conn_data


# Get Network connection on system
def network_task():
    network_data = list()
    if platform.system() in ["Windows", "Linux", "Darwin"]:
        network_data = get_network_connection()
    else:
        network_data.append("Operating system is not detected.")
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)
    write_dicts_to_json_file(network_data, "network.json")
    return len(network_data)
