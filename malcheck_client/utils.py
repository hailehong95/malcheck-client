import os
import json
import struct
import ctypes
import socket
import urllib
import hashlib
import zipfile
import requests
import binascii
import platform
import subprocess
import geoip2.database

from datetime import datetime
from malcheck_client.logging import logger
from malcheck_client.crypto import string_random
from malcheck_client.config import BINS_DIR, DATA_DIR, KEYS_DIR, BASE_DIR
from malcheck_client.config import SYSINTERNAL_SIGCHECK, MAX_SIZE_FILE, CWD_DIR


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def get_primary_ip_without_internet(host="10.255.255.255", port=1):
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sk.connect((host, port))
        primary_ip = sk.getsockname()[0]
    except Exception:
        primary_ip = "127.0.0.1"
    finally:
        sk.close()
    return primary_ip


def get_primary_ip_with_internet(host="www.google.com", port=80, timeout=5):
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sk.settimeout(timeout)
        sk.connect((socket.gethostbyname(host), port))
        primary_ip = sk.getsockname()[0]
    except:
        primary_ip = "127.0.0.1"
    finally:
        sk.close()
    return primary_ip


def internet_check_by_urllib(url="http://www.google.com/", timeout=5):
    try:
        _ = urllib.request.urlopen(url, timeout=timeout)
        return True
    except:
        pass
    return False


def internet_check_by_requests(url="http://www.google.com/", timeout=5):
    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        pass
    return False


def internet_check_by_socket(host="8.8.8.8", port=53, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        pass
    return False


# Check Signature of PE File
def pe_signature_check(pe_file):
    try:
        data = dict()
        sigcheck_cmd = [SYSINTERNAL_SIGCHECK, "-accepteula", "-nobanner", pe_file]
        sigcheck_output = subprocess.run(sigcheck_cmd, stdout=subprocess.PIPE)
        sigcheck_output = sigcheck_output.stdout.decode("utf-8", errors="ignore").replace("\t", "").splitlines()

        data["verified"] = sigcheck_output[1].split(":")[-1]
        data["signing_date"] = sigcheck_output[2].split("ate:")[-1]
        data["publisher"] = sigcheck_output[3].split(":")[-1]
        data["machine_type"] = sigcheck_output[9].split(":")[-1]
    except Exception as ex:
        logger.info(str(ex))
    else:
        return data


def get_hash_file(file):
    try:
        hash_data = dict()
        hash_md5 = hashlib.md5()
        hash_sha1 = hashlib.sha1()
        hash_sha256 = hashlib.sha256()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
                hash_sha1.update(chunk)
                hash_sha256.update(chunk)
        hash_data["md5"] = hash_md5.hexdigest()
        hash_data["sha1"] = hash_sha1.hexdigest()
        hash_data["sha256"] = hash_sha256.hexdigest()
    except Exception as ex:
        logger.info(str(ex))
    else:
        return hash_data


def is_valid_file(file):
    if os.path.getsize(file) > MAX_SIZE_FILE:
        return False
    extension = [".exe", ".dll", ".sys", ".drv", ".ocx", ".cpl", ".scr", ".com"]
    for ext in extension:
        if file.endswith(ext):
            return True
    try:
        pe_header = b''
        with open(file, 'rb') as fs:
            pe_header = binascii.hexlify(fs.read()[:4])
        if b'4d5a' in pe_header:
            return True
    except Exception as ex:
        logger.info(str(ex))
    return False


def get_file_recursively(path):
    list_file = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            list_file.append(os.path.join(root, file))
    return list_file


def write_dicts_to_json_file(dict_data, file_name):
    try:
        with open(os.path.join(DATA_DIR, file_name), "w") as fs:
            json.dump(dict_data, fs)
    except Exception as ex:
        logger.info(str(ex))


def zip_list_file():
    try:
        json_file = list()
        if os.path.exists(DATA_DIR):
            for x in os.listdir(DATA_DIR):
                if x.endswith(".json"):
                    json_file.append(x)
        # tmp_name = "-".join([platform.node(), string_random(6) + ".zip"])
        tmp_name = "-".join(
            [platform.system().lower(), platform.node().lower(), datetime.now().strftime("%Y%m%d%H%M%S") + ".zip"])
        zip_name = os.path.join(CWD_DIR, tmp_name)
        os.chdir(DATA_DIR)
        with zipfile.ZipFile(zip_name, "w") as zipObj:
            for file_ in json_file:
                zipObj.write(file_)
        return zip_name
    except Exception as ex:
        logger.info(str(ex))
    finally:
        os.chdir(BASE_DIR)


# Ref: https://stackoverflow.com/a/39656628/20555382
def is_private_ip(ip):
    networks = [
        "0.0.0.0/8",
        "10.0.0.0/8",
        "100.64.0.0/10",
        "127.0.0.0/8",
        "169.254.0.0/16",
        "172.16.0.0/12",
        "192.0.0.0/24",
        "192.0.2.0/24",
        "192.88.99.0/24",
        "192.168.0.0/16",
        "198.18.0.0/15",
        "198.51.100.0/24",
        "203.0.113.0/24",
        "240.0.0.0/4",
        "255.255.255.255/32",
        "224.0.0.0/4",
    ]
    for network in networks:
        try:
            ipaddr = struct.unpack(">I", socket.inet_aton(ip))[0]
            netaddr, bits = network.split("/")
            network_low = struct.unpack(">I", socket.inet_aton(netaddr))[0]
            network_high = network_low | 1 << (32 - int(bits)) - 1
            if ipaddr <= network_high and ipaddr >= network_low:
                return True
        except Exception as ex:
            continue
    return False


def geoip_country(db_path, ip_list):
    ip_country = dict()
    ips = list(set(ip_list))
    for ip in ips:
        try:
            if ip == "unknown":
                ip_country[ip] = "unknown"
            elif is_private_ip(ip):
                ip_country[ip] = "unknown"
            else:
                with geoip2.database.Reader(db_path) as reader:
                    response = reader.country(ip)
                ip_country[ip] = response.country.name
        except Exception as ex:
            ip_country[ip] = "unknown"
            logger.info(str(ex))
    return ip_country
