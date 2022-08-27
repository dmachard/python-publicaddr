
import requests

NAME = "Akamai"

timeout = 5

http_servers = {
    "ip4": "http://ipv4.whatismyip.akamai.com/",
    "ip6": "http://ipv6.whatismyip.akamai.com/",
}

def lookup(ipversion, ipproto):
    ret = None
    try:
        if ipversion == 4:
            ret = requests.get(http_servers["ip4"], timeout=timeout).text.rstrip()
        if ipversion == 6:
            ret = requests.get(http_servers["ip6"], timeout=timeout).text.rstrip()
    except requests.exceptions.RequestException:
        pass
    return ret