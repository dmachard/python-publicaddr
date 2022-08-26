
import dns.resolver
import dns.exception

NAME = "OpenDNS"

# resolver1.opendns.com, resolver2.opendns.com
dns_servers = {
    "ip4": ["208.67.222.222", "208.67.220.220"],
    "ip6": ["2620:119:35::35", "2620:119:53::53"],
}

# dig myip.opendns.com @resolver1.opendns.com -6 AAAA +short
# dig myip.opendns.com @resolver1.opendns.com -4 A +short

def _resolv_addr(nameservers=[], qname="myip.opendns.com", rdtype="A"):
    dnsresolv = dns.resolver.Resolver(configure=False)
    dnsresolv.nameservers = nameservers

    # make dns resolution
    answers = dnsresolv.resolve(qname, rdtype)
    return answers[0].to_text()

def lookup(ipversion, ipproto):
    ret = None
    try:
        if ipversion == 4:
            return _resolv_addr(nameservers=dns_servers["ip4"], rdtype="A")
        if ipversion == 6:
            return _resolv_addr(nameservers=dns_servers["ip6"], rdtype="AAAA")
    except dns.exception.DNSException:
        pass
    return ret