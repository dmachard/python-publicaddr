
import logging
import requests
import aiostun
import dns.resolver
import dns.exception
import asyncio

from publicaddr import constants

NAME = "Matrix"

timeout = 5

dns_servers = {}

http_servers = {}

stuns_servers = {
    "ip4": "turn.matrix.org",
    "ip6": "turn.matrix.org",
}

async def _lookup_stun(ipversion):
    if ipversion == 4:
        async with aiostun.Client(host=stuns_servers["ip4"], port=443, family=aiostun.IP4, proto=aiostun.TLS) as stunc:
            mapped_addr = await stunc.get_mapped_address()
    if ipversion == 6:
        async with aiostun.Client(host=stuns_servers["ip6"], port=443, family=aiostun.IP6, proto=aiostun.TLS) as stunc:
            mapped_addr = await stunc.get_mapped_address()
    return mapped_addr

def lookup_stun(ipversion):
    ip = None
    try:
        mapped_addr = asyncio.run(_lookup_stun(ipversion))
        ip = mapped_addr["ip"]
    except Exception as e:
        logging.error("matrix unable to get stun ip info - %s" % e)
    return ip

def lookup(ipversion, ipproto):
    ret = None

    if ipproto == constants.PROTO_STUNS:
        ret = lookup_stun(ipversion)

    else:
        logging.error("matrix lookup invalid ipproto - %s" % ipproto)

    return ret