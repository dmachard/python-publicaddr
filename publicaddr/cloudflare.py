
import dns.resolver

# resolver1.opendns.com, resolver2.opendns.com
dns_servers = {
    "ip4": ["1.1.1.1", "1.0.0.1"],
    "ip6": ["2606:4700:4700::1111", "2606:4700:4700::1001"],
}

# dig @2606:4700:4700::1111 whoami.cloudflare TXT CH +short
# dig @2606:4700:4700::1111 whoami.cloudflare TXT CH +short
def _resolv_addr(nameservers=[], qname="whoami.cloudflare", rdtype="TXT", rdclass="CH"  ):
    dnsresolv = dns.resolver.Resolver(configure=False)
    dnsresolv.nameservers = nameservers

    # make dns resolution
    answers = dnsresolv.resolve(qname, rdtype, rdclass)
    return answers[0].strings[0].decode()

def lookup(ipversion, ipproto):
    if ipversion == 4:
        return _resolv_addr(nameservers=dns_servers["ip4"])
    if ipversion == 6:
        return _resolv_addr(nameservers=dns_servers["ip6"])