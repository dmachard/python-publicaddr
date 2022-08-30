
import requests
import dns.resolver
import dns.exception
import logging

from publicaddr import constants

NAME = "Akamai"
HAS_DNS_SUPPORT = False
HAS_HTTP_SUPPORT = True

timeout = 1

# a1-67.akam.net, a3-67.akam.net
dns_servers = {
    "ip4": ["193.108.91.67", "96.7.49.67"],
    "ip6": ["2600:1401:2::43", "2600:1408:1c::43"]
}

http_servers = {
    "ip4": "http://ipv4.whatismyip.akamai.com/",
    "ip6": "http://ipv6.whatismyip.akamai.com/",
}


# dig @193.108.91.67 whoami.ds.akahelp.net TXT +short
# "ns" "x.x.x.x"
def _resolv_addr(nameservers=[], qname="whoami.ds.akahelp.net", rdtype="TXT"):
    dnsresolv = dns.resolver.Resolver(configure=False)
    dnsresolv.nameservers = nameservers
    dnsresolv.timeout = timeout
    dnsresolv.lifetime = timeout

    answers = dnsresolv.resolve(qname, rdtype)
    return answers[0].strings[1].decode()

def lookup_dns(ipversion):
    ip = None
    try:
        if ipversion == 4:
            ip = _resolv_addr(nameservers=dns_servers["ip4"])
        if ipversion == 6:
            ip = _resolv_addr(nameservers=dns_servers["ip6"])
    except dns.exception.DNSException as e:
        logging.error("akamai unable to get ip info - %s" % e)
    return ip

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

    if ipproto == constants.PROTO_DNS:
        ret = lookup_dns(ipversion)

    elif ipproto == constants.PROTO_HTTP:
        ret = lookup_http(ipversion)
        
    else:
        logging.error("akamai lookup invalid ipproto - %s" % ipproto)
           
    return ret