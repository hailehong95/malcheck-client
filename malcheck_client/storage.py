import requests
from malcheck_client.logging import logger
from malcheck_client.config import MALCHECK_WEBSERVER


def get_pre_signed_url(object_name):
    try:
        res = requests.post(MALCHECK_WEBSERVER, json={"object_name": object_name})
        pre_signed_url = res.json().get("url")
        return pre_signed_url
    except Exception as ex:
        logger.info(str(ex))


def pre_signed_upload(pre_signed_url, obj_path):
    try:
        data = open(obj_path, "rb").read()
        headers = {"Content-Type": "application/binary", }
        r = requests.put(pre_signed_url, data=data, headers=headers)
        return r.status_code == 200
    except Exception as ex:
        logger.info(str(ex))
        return False
