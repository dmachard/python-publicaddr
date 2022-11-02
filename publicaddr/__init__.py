
import logging
import sys
import time
import pkgutil
import yaml
import re

from publicaddr import constants
from publicaddr.constants import *
from publicaddr import randprov
from publicaddr import handlers

cfg = {}

def lookup(providers=constants.ALL, retries=None, timeout=None):
    """lookup for all public IP if existsfrom random providers"""
    global cfg
    if retries is not None: cfg["retries"] = retries
    if timeout is not None: cfg["timeout"] = timeout
    logging.debug("lookup from providers retries=%s" % (cfg["retries"]))

    addrs = {}

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

        if provider["mode"] == constants.HTTPS:
            insecure = False
            if "insecure" in provider:
                insecure = provider["insecure"]
            addrs["ip4"] = handlers.lookup_http(url=provider["url"], ipversion=constants.IPv4,
                                                timeout=cfg["timeout"], insecure=insecure)
            addrs["ip6"] = handlers.lookup_http(url=provider["url"], ipversion=constants.IPv6,
                                                timeout=cfg["timeout"], insecure=insecure)

        if provider["mode"] == constants.DNS:
            dnsclass = provider["class"] if "class" in provider else "IN"
            qtype = provider["qtype"] if "qtype" in provider else None
            pattern = provider["pattern"] if "pattern" in provider else None

            addrs["ip4"] = handlers.lookup_dns_v4(nameservers=provider["nameservers"],
                                                  lookup=provider["lookup"],
                                                  dnsclass=dnsclass, qtype=qtype,
                                                  timeout=cfg["timeout"], pattern=pattern)
            addrs["ip6"] = handlers.lookup_dns_v6(nameservers=provider["nameservers"],
                                                  lookup=provider["lookup"],
                                                  dnsclass=dnsclass, qtype=qtype,
                                                  timeout=cfg["timeout"], pattern=pattern)

        if provider["mode"] == constants.STUN:
            addrs["ip4"] = handlers.lookup_stun(host=provider["host"], port=provider["port"], 
                                                ipversion=constants.IPv4,
                                                transport=provider["transport"],
                                                timeout=cfg["timeout"])
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

    if _provider["mode"] == constants.HTTPS:
        insecure = _provider["insecure"] if "insecure" in _provider else False
        pattern = _provider["pattern"] if "pattern" in _provider else None
        addr["ip"] = handlers.lookup_http(url=_provider["url"], ipversion=ip,
                                          timeout=cfg["timeout"], insecure=insecure,
                                          pattern=pattern)

    if _provider["mode"] == constants.DNS:
        dnsclass = _provider["class"] if "class" in _provider else "IN"
        qtype = _provider["qtype"] if "qtype" in _provider else None
        pattern = _provider["pattern"] if "pattern" in _provider else None

        dns_handler = handlers.lookup_dns_v4
        if ip == constants.IPv6:
            dns_handler = handlers.lookup_dns_v6
        addr["ip"] = dns_handler(nameservers=_provider["nameservers"], lookup=_provider["lookup"],
                                 dnsclass=dnsclass, qtype=qtype, timeout=cfg["timeout"], pattern=pattern)

    if _provider["mode"] == constants.STUN:
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