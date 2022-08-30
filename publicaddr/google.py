
import logging
import requests

import dns.resolver
import dns.exception

from publicaddr import constants

NAME = "Google"

timeout = 5

 # ns1.google.com, ns2.google.com, ns3.google.com
dns_servers = {
    "ip4": ["216.239.32.10", "216.239.34.10", "216.239.36.10"],
    "ip6": ["2001:4860:4802:32::a", "2001:4860:4802:34::a", "2001:4860:4802:36::a"],
}

http_servers = {
    "ip4": "https://domains.google.com/checkip",
    "ip6": "https://domains.google.com/checkip",
}

def _resolv_addr(nameservers=[], qname="o-o.myaddr.google.com", rdtype="TXT" ):
    dnsresolv = dns.resolver.Resolver(configure=False)
    dnsresolv.nameservers = nameservers
    dnsresolv.timeout = timeout
    dnsresolv.lifetime = timeout

    # make dns resolution
    answers = dnsresolv.resolve(qname, rdtype)
    return answers[0].strings[0].decode()

def lookup_dns(ipversion):
    ip = None
    try:
        if ipversion == 4:
            ip = _resolv_addr(nameservers=dns_servers["ip4"])
        if ipversion == 6:
            ip = _resolv_addr(nameservers=dns_servers["ip6"])
    except dns.exception.DNSException as e:
        logging.error("google unable to get dns ip info - %s" % e)
    return ip

def lookup_http(ipversion):
    ip = None
    try:
        if ipversion == 4:
            requests.packages.urllib3.util.connection.HAS_IPV6 = False
            ip = requests.get(http_servers["ip4"], timeout=timeout).text.rstrip()
        if ipversion == 6:
            requests.packages.urllib3.util.connection.HAS_IPV6 = True
            ip = requests.get(http_servers["ip6"], timeout=timeout).text.rstrip()
    except requests.exceptions.RequestException as e:
        logging.error("google unable to get http ip info - %s" % e)
    return ip

def lookup(ipversion, ipproto):
    ret = None

    if ipproto == constants.PROTO_DNS:
        ret = lookup_dns(ipversion)

    elif ipproto == constants.PROTO_HTTP:
        ret = lookup_http(ipversion)
        
    else:
        logging.error("google lookup invalid ipproto - %s" % ipproto)

    return ret