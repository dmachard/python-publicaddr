
from publicaddr import google
from publicaddr import opendns
from publicaddr import cloudflare
from publicaddr import akamai

from publicaddr import randprov

# Use IPv4 or IPv6 protocols to reach the provider
IP_V4=4
IP_V6=6

# Use DNS or HTTP protocols to reach the provider
PROTO_DNS=1
PROTO_HTTP=2

# the default provider
PROVIDER_RANDOM = randprov

# the list of available providers
PROVIDER_GOOGLE = google
PROVIDER_OPENDNS = opendns
PROVIDER_CLOUDFLARE = cloudflare
PROVIDER_AKAMAI = akamai

# register providers
randprov.set_providers([google, opendns, cloudflare, akamai])

# get all public IP if exists
def getall(provider=PROVIDER_RANDOM, ipproto=PROTO_DNS):
    """return your public ipv4 and ipv6"""
    _provider = provider
    # select provider in random mode ?
    if provider == PROVIDER_RANDOM: _provider = provider.pickone()

    # lookup for public all ip
    addrs = {}
    addrs["ip4"] = _provider.lookup(ipversion=IP_V4, ipproto=ipproto)
    addrs["ip6"] = _provider.lookup(ipversion=IP_V6, ipproto=ipproto)
    addrs["provider"] = _provider.NAME
    return addrs

# return from a specific provider, the IPv4 or IPv6
def get(provider=PROVIDER_RANDOM, ipversion=IP_V4, ipproto=PROTO_DNS):
    """return your public ipv4 or ipv6"""
    _provider = provider
    # select provider in random mode ?
    if provider == PROVIDER_RANDOM: _provider = provider.pickone()

    # lookup for public ip
    addr = {}
    addr["ip"] = _provider.lookup(ipversion=ipversion, ipproto=ipproto)
    addr["provider"] = _provider.NAME
    return addr