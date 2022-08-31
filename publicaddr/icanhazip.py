import requests
import logging

from publicaddr import constants

NAME = "Icanhazip"

timeout = 1

dns_servers = {}

http_servers = {
    "ip4": "https://ipv4.icanhazip.com/",
    "ip6": "https://ipv6.icanhazip.com/",
}

def lookup_http(ipversion):
    ip = None
    try:
        if ipversion == 4:
            ip = requests.get(http_servers["ip4"], timeout=timeout).text.rstrip()
        if ipversion == 6:
            ip = requests.get(http_servers["ip6"], timeout=timeout).text.rstrip()
    except requests.exceptions.RequestException as e:
        logging.error("icanhazip unable to get ip info - %s" % e)
    return ip

def lookup(ipversion, ipproto):
    ret = None

    if ipproto == constants.PROTO_HTTP:
        ret = lookup_http(ipversion)
        
    else:
        logging.error("icanhazip lookup invalid ipproto - %s" % ipproto)
           
    return ret