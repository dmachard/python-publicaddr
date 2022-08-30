
import dns.resolver
import dns.exception
import logging

from publicaddr import constants

NAME = "Cloudflare"
HAS_DNS_SUPPORT = True
HAS_HTTP_SUPPORT = False

timeout = 1

# resolver1.opendns.com, resolver2.opendns.com
dns_servers = {
    "ip4": ["1.1.1.1", "1.0.0.1"],
    "ip6": ["2606:4700:4700::1111", "2606:4700:4700::1001"],
}

http_servers = {}

# dig @2606:4700:4700::1111 whoami.cloudflare TXT CH +short
# dig @2606:4700:4700::1111 whoami.cloudflare TXT CH +short
def _resolv_addr(nameservers=[], qname="whoami.cloudflare", rdtype="TXT", rdclass="CH"  ):
    dnsresolv = dns.resolver.Resolver(configure=False)
    dnsresolv.nameservers = nameservers
    dnsresolv.timeout = timeout
    dnsresolv.lifetime = timeout
    
    # make dns resolution
    answers = dnsresolv.resolve(qname, rdtype, rdclass)
    return answers[0].strings[0].decode()

def lookup_dns(ipversion):
    ip = None
    try:
        if ipversion == 4:
            ip = _resolv_addr(nameservers=dns_servers["ip4"])
        if ipversion == 6:
            ip = _resolv_addr(nameservers=dns_servers["ip6"])
    except dns.exception.DNSException as e:
        logging.error("cloudflare unable to get ip info - %s" % e)
    return ip

def lookup(ipversion, ipproto):
    ret = None

    if ipproto == constants.PROTO_DNS:
        ret = lookup_dns(ipversion)
        
    else:
        logging.error("cloudflare lookup invalid ipproto - %s" % ipproto)
           
    return ret