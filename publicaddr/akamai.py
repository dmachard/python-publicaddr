
import requests

http_servers = {
    "ip4": "http://ipv4.whatismyip.akamai.com/",
    "ip6": "http://ipv6.whatismyip.akamai.com/",
}

def lookup(ipversion, ipproto):
    if ipversion == 4:
        return requests.get(http_servers["ip4"]).text.rstrip()
    if ipversion == 6:
        return requests.get(http_servers["ip6"]).text.rstrip()