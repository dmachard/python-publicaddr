
from publicaddr import google
from publicaddr import opendns
from publicaddr import cloudflare
from publicaddr import akamai

PROVIDER_GOOGLE = google
PROVIDER_OPENDNS = opendns
PROVIDER_CLOUDFLARE = cloudflare
PROVIDER_AKAMAI = akamai

IP_V4=4
IP_V6=6

PROTO_DNS=1
PROTO_HTTP=2

def getall(provider=PROVIDER_GOOGLE, ipproto=PROTO_DNS):
    """return your public ipv4 and ipv6"""
    addrs = {}
    addrs["ip4"] = provider.lookup(ipversion=IP_V4, ipproto=ipproto)
    addrs["ip6"] = provider.lookup(ipversion=IP_V6, ipproto=ipproto)
    return addrs

def get(provider=PROVIDER_GOOGLE, ipversion=IP_V4, ipproto=PROTO_DNS):
    """return your public ipv4 or ipv6"""
    return provider.lookup(ipversion=ipversion, ipproto=ipproto)