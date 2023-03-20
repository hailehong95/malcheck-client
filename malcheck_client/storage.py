import requests
from malcheck_client.logging import logger
from malcheck_client.utils import gen_token_hex
from malcheck_client.config import MALCHECK_BASE_URL


def user_checkin(user_info):
    try:
        url = f"{MALCHECK_BASE_URL}/api/v1/checkin"
        data = dict(user_info)
        hex_token = gen_token_hex(16)
        data['signature'] = hex_token
        res = requests.post(url, json=data)
        return res.status_code, hex_token
    except Exception as ex:
        logger.info(str(ex))
        return -1, ''


def user_checkout(user_info, hex_token):
    try:
        url = f"{MALCHECK_BASE_URL}/api/v1/checkout"
        name = user_info['name']
        emp_id = user_info['emp_id']
        address = user_info['address']
        data = {'name': name, 'emp_id': emp_id, 'address': address, 'signature': hex_token}
        res = requests.post(url, json=data)
        return res.status_code == 200
    except Exception as ex:
        logger.info(str(ex))
        return False


def user_get_upload_url(object_name):
    try:
        url = f"{MALCHECK_BASE_URL}/api/v1/upload"
        res = requests.post(url, json={"object_name": object_name})
        pre_signed_url = res.json().get("url")
        return pre_signed_url
    except Exception as ex:
        logger.info(str(ex))


def user_upload(pre_signed_url, obj_path):
    try:
        data = open(obj_path, "rb").read()
        headers = {"Content-Type": "application/binary", }
        r = requests.put(pre_signed_url, data=data, headers=headers)
        return r.status_code == 200
    except Exception as ex:
        logger.info(str(ex))
        return False
