
import logging

import dns.resolver
import dns.exception

NAME = "Google"
timeout = 1

 # ns1.google.com, ns2.google.com, ns3.google.com
dns_servers = {
    "ip4": ["216.239.32.10", "216.239.34.10", "216.239.36.10"],
    "ip6": ["2001:4860:4802:32::a", "2001:4860:4802:34::a", "2001:4860:4802:36::a"],
}

def _resolv_addr(nameservers=[], qname="o-o.myaddr.google.com", rdtype="TXT" ):
    dnsresolv = dns.resolver.Resolver(configure=False)
    dnsresolv.nameservers = nameservers
    dnsresolv.timeout = timeout
    dnsresolv.lifetime = timeout

    # make dns resolution
    answers = dnsresolv.resolve(qname, rdtype)
    return answers[0].strings[0].decode()

def lookup(ipversion, ipproto, debug):
    ret = None
    try:
        if ipversion == 4:
            return _resolv_addr(nameservers=dns_servers["ip4"])
        if ipversion == 6:
            return _resolv_addr(nameservers=dns_servers["ip6"])
    except dns.exception.DNSException as e:
        if debug: logging.debug("google unable to get ip info - %s" % e)
    return ret