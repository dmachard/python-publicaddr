
import requests
import logging

from publicaddr import constants

NAME = "Akamai"
HAS_DNS_SUPPORT = False
HAS_HTTP_SUPPORT = True

timeout = 5

dns_servers = {}

http_servers = {
    "ip4": "http://ipv4.whatismyip.akamai.com/",
    "ip6": "http://ipv6.whatismyip.akamai.com/",
}

def lookup_http(ipversion):
    ip = None
    try:
        if ipversion == 4:
            ip = requests.get(http_servers["ip4"], timeout=timeout).text.rstrip()
        if ipversion == 6:
            ip = requests.get(http_servers["ip6"], timeout=timeout).text.rstrip()
    except requests.exceptions.RequestException as e:
        logging.error("akamai unable to get ip info - %s" % e)
    return ip

def lookup(ipversion, ipproto):
    ret = None

    if ipproto == constants.PROTO_HTTP:
        ret = lookup_http(ipversion)
        
    else:
        logging.error("akamai lookup invalid ipproto - %s" % ipproto)
           
    return ret