
import logging
import sys
import time
import pkgutil
import yaml
import re
import os

from publicaddr import constants
from publicaddr.constants import *
from publicaddr import randprov
from publicaddr import handlers

cfg = {}

def lookup(providers=constants.ALL, retries=None, timeout=None, ip=None):
    """lookup for all public IP if existsfrom random providers"""
    global cfg
    if retries is not None: cfg["retries"] = retries
    if timeout is not None: cfg["timeout"] = timeout
    logging.debug("lookup from providers retries=%s" % (cfg["retries"]))

    addrs = {"ip4": None, "ip6": None}

    for _ in range(cfg["retries"]):
        start = time.perf_counter()

        if providers == constants.ALL:
            provider = randprov.pick_all()
        elif providers == constants.HTTPS:
            provider = randprov.pick_https()
        elif providers == constants.DNS:
            provider = randprov.pick_dns()
        elif providers == constants.STUN:
            provider = randprov.pick_stun()
        else:
            logging.error("fetch invalid providers - %s" % providers)
            return addrs

        if provider["mode"] == constants.HTTPS and cfg["https_enabled"]:
            insecure = False
            ipv6_support = cfg["ipv6_enabled"]
            pattern = provider["pattern"] if "pattern" in provider else None

            if "insecure" in provider:
                insecure = provider["insecure"]
            if "ipv6_support" in provider:
                ipv6_support = provider["ipv6_support"]

            if ip == constants.IPv4 or ip == None:
                addrs["ip4"] = handlers.lookup_http(url=provider["url"], ipversion=constants.IPv4,
                                                    timeout=cfg["timeout"], insecure=insecure,
                                                    pattern=pattern, ipv6_support=ipv6_support)
            if (ip == constants.IPv6 or ip == None ) and cfg["ipv6_enabled"]:
                addrs["ip6"] = handlers.lookup_http(url=provider["url"], ipversion=constants.IPv6,
                                                    timeout=cfg["timeout"], insecure=insecure,
                                                    pattern=pattern, ipv6_support=ipv6_support)

        if provider["mode"] == constants.DNS and cfg["dns_enabled"]:
            dnsclass = provider["class"] if "class" in provider else "IN"
            qtype = provider["qtype"] if "qtype" in provider else None
            pattern = provider["pattern"] if "pattern" in provider else None

            if ip == constants.IPv4 or ip == None:
                addrs["ip4"] = handlers.lookup_dns_v4(nameservers=provider["nameservers"],
                                                    lookup=provider["lookup"],
                                                    dnsclass=dnsclass, qtype=qtype,
                                                    timeout=cfg["timeout"], pattern=pattern)
            if (ip == constants.IPv6 or ip == None)  and cfg["ipv6_enabled"]:
                addrs["ip6"] = handlers.lookup_dns_v6(nameservers=provider["nameservers"],
                                                    lookup=provider["lookup"],
                                                    dnsclass=dnsclass, qtype=qtype,
                                                    timeout=cfg["timeout"], pattern=pattern)

        if provider["mode"] == constants.STUN and cfg["stun_enabled"]:
            if ip == constants.IPv4 or ip == None:
                addrs["ip4"] = handlers.lookup_stun(host=provider["host"], port=provider["port"], 
                                                    ipversion=constants.IPv4,
                                                    transport=provider["transport"],
                                                    timeout=cfg["timeout"])
            if (ip == constants.IPv6 or ip == None) and cfg["ipv6_enabled"]:
                addrs["ip6"] = handlers.lookup_stun(host=provider["host"], port=provider["port"], 
                                                    ipversion=constants.IPv6,
                                                    transport=provider["transport"],
                                                    timeout=cfg["timeout"])

        addrs["provider"] = provider["name"]
        addrs["proto"] = provider["mode"]

        request_time = time.perf_counter() - start
        addrs["duration"] = "{0:.3f}".format(request_time)

        if not(addrs["ip4"] is None and addrs["ip6"] is None):
            break
    return addrs

def _get_provider(name, proto):
    global cfg

    if proto == constants.HTTPS:
        for prov in cfg["providers"][constants.HTTPS]:
            if prov["name"] == name:
                return prov
        return None

    elif proto == constants.DNS:
        for prov in cfg["providers"][constants.DNS]:
            if prov["name"] == name:
                return prov
        return None

    elif proto == constants.STUN:
        for prov in cfg["providers"][constants.STUN]:
            if prov["name"] == name:
                return prov
        return None

    else:
        logging.error("invalid proto - %s" % proto)
        return None

def get(provider="google", proto=constants.DNS, ip=constants.IPv4, timeout=None):
    global cfg
    if timeout is not None: cfg["timeout"] = timeout

    # search provider
    _provider = _get_provider(provider, proto) 
    if _provider is None: return None
        
    logging.debug("get from provider=%s ipversion=%s ipproto=%s" % (_provider["name"], ip, _provider["mode"]))

    start = time.perf_counter()
    addr = {}

    if ip == constants.IPv6 and not cfg["ipv6_enabled"]:
        addr["ip"] = None
        addr["duration"] = "0"
        return addr

    if _provider["mode"] == constants.HTTPS and cfg["https_enabled"]:
        insecure = _provider["insecure"] if "insecure" in _provider else False
        pattern = _provider["pattern"] if "pattern" in _provider else None
        ipv6_support = cfg["ipv6_enabled"]
        if "ipv6_support" in _provider:
            ipv6_support = bool(_provider["ipv6_support"] )
        addr["ip"] = handlers.lookup_http(url=_provider["url"], ipversion=ip,
                                          timeout=cfg["timeout"], insecure=insecure,
                                          pattern=pattern, ipv6_support=ipv6_support)

    if _provider["mode"] == constants.DNS and cfg["dns_enabled"]:
        dnsclass = _provider["class"] if "class" in _provider else "IN"
        qtype = _provider["qtype"] if "qtype" in _provider else None
        pattern = _provider["pattern"] if "pattern" in _provider else None

        dns_handler = handlers.lookup_dns_v4
        if ip == constants.IPv6:
            dns_handler = handlers.lookup_dns_v6
        addr["ip"] = dns_handler(nameservers=_provider["nameservers"], lookup=_provider["lookup"],
                                 dnsclass=dnsclass, qtype=qtype, timeout=cfg["timeout"], pattern=pattern)

    if _provider["mode"] == constants.STUN and cfg["stun_enabled"]:
        addr["ip"] = handlers.lookup_stun(host=_provider["host"], port=_provider["port"], ipversion=ip, 
                                          transport=_provider["transport"], timeout=cfg["timeout"])

    request_time = time.perf_counter() - start
    addr["duration"] = "{0:.3f}".format(request_time)
    return addr

def load_cfg():
    """read default config or from file"""
    cfg = None
    try:
        conf = pkgutil.get_data(__package__, 'publicaddr.yml')
        cfg =  yaml.safe_load(conf) 
    except Exception as e:
        logging.error("invalid default config: %s" % e)

    # load from env
    debug_env = os.getenv('PUBLICADDR_DEBUG')
    if debug_env is not None: cfg["debug"] = bool( int(debug_env) )

    timeout_env = os.getenv('PUBLICADDR_TIMEOUT')
    if timeout_env is not None: cfg["timeout"] = int(timeout_env)

    retries_env = os.getenv('PUBLICADDR_RETRIES')
    if retries_env is not None: cfg["retries"] = int(retries_env)

    https_enable_env = os.getenv('PUBLICADDR_LOOKUP_HTTPS')
    if https_enable_env is not None: cfg["https_enabled"] = bool(int(https_enable_env))

    dns_enable_env = os.getenv('PUBLICADDR_LOOKUP_DNS')
    if dns_enable_env is not None: cfg["dns_enabled"] = bool(int(dns_enable_env))

    stun_enable_env = os.getenv('PUBLICADDR_LOOKUP_STUN')
    if stun_enable_env is not None: cfg["stun_enabled"] = bool(int(stun_enable_env))

    ipv6_enable_env = os.getenv('PUBLICADDR_IPV6_ENABLED')
    if ipv6_enable_env is not None: cfg["ipv6_enabled"] = bool(int(ipv6_enable_env))

    return cfg

def init():
    """load default providers"""
    global cfg
    _cfg = load_cfg()
    if _cfg is None: return
    cfg = _cfg

    if cfg["debug"]:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.ERROR

    logging.getLogger("requests").setLevel(loglevel)
    logging.getLogger("urllib3").setLevel(loglevel)
    logging.basicConfig(format='%(levelname)s %(message)s', stream=sys.stdout, level=loglevel)

    # load default providers
    pattern = r"[^A-Za-z0-9]+"
    for proto, providers in cfg["providers"].items():

        for prov in providers:
            if prov["name"] not in globals():
                prov_name = re.sub(pattern, '_', prov["name"].upper())
                globals()[prov_name] = prov["name"]

        if proto == constants.HTTPS:
            randprov.set_http_providers(providers)
        if proto == constants.DNS:
            randprov.set_dns_providers(providers)
        if proto == constants.STUN:
            randprov.set_stun_providers(providers)

init()