
import logging
import sys
import time

from publicaddr import google as PROVIDER_GOOGLE
from publicaddr import opendns as PROVIDER_OPENDNS
from publicaddr import cloudflare as PROVIDER_CLOUDFLARE
from publicaddr import akamai as PROVIDER_AKAMAI

from publicaddr import randprov
from publicaddr import constants

from publicaddr.constants import *

loglevel = logging.INFO
logging.basicConfig(format='%(asctime)s %(message)s', stream=sys.stdout, level=loglevel)
logging.getLogger("requests").setLevel(loglevel)
logging.getLogger("urllib3").setLevel(loglevel)

# register providers
randprov.set_providers([PROVIDER_GOOGLE, PROVIDER_OPENDNS, 
                        PROVIDER_CLOUDFLARE, PROVIDER_AKAMAI])

# get all public IP if exists
def lookup(providers=constants.ALL_PROVIDERS):
    """lookup your public ipv4 and ipv6 from random providers"""
    addrs = {}
    start = time.perf_counter()

    # select provider in random mode
    if providers == constants.ALL_PROVIDERS: 
        _provider = randprov.pick_all()
        if len(_provider.dns_servers) and not len(_provider.http_servers): 
            _ipproto = constants.PROTO_DNS
        elif not len(_provider.dns_servers) and len(_provider.http_servers): 
            _ipproto = constants.PROTO_HTTP
        else:
            _ipproto = randprov.pick_proto()

    elif providers == constants.DNS_PROVIDERS: 
        _provider = randprov.pick_dns()
        _ipproto = constants.PROTO_DNS

    elif providers == constants.HTTP_PROVIDERS: 
        _provider = randprov.pick_http()
        _ipproto = constants.PROTO_HTTP

    else:
        logging.error("fetch invalid providers mode - %s" % providers)
        return addrs

    # lookup for public all ip
    addrs["ip4"] = _provider.lookup(ipversion=constants.IP_V4, ipproto=_ipproto)
    addrs["ip6"] = _provider.lookup(ipversion=constants.IP_V6, ipproto=_ipproto)
    addrs["provider"] = _provider.NAME
    addrs["proto"] = constants.PROTO_STR[_ipproto]

    request_time = time.perf_counter() - start
    addrs["duration"] = "{0:.3f}".format(request_time)

    return addrs

# return from a specific provider, the IPv4 or IPv6
def get(provider=PROVIDER_GOOGLE, ipversion=constants.IP_V4, ipproto=constants.PROTO_DNS):
    """return your public ipv4 or ipv6"""
    start = time.perf_counter()
    addr = {}
    addr["ip"] = provider.lookup(ipversion=ipversion, ipproto=ipproto)
    request_time = time.perf_counter() - start
    addr["duration"] = "{0:.3f}".format(request_time)
    return addr

