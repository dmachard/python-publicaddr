
from dataclasses import dataclass
import requests
import logging
import asyncio
import aiostun
import re
import socket

import dns.resolver
import dns.exception

from publicaddr import constants

import checkifvalid

# Suppress only the single warning from urllib3 needed.
from urllib3.exceptions import InsecureRequestWarning

def lookup_http(url, ipversion, timeout, insecure, pattern, ipv6_support):
    ip = None
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    try:
        if ipversion == constants.IPv4:
            def allowed_gai_family():
                return socket.AF_INET
        else:
            if not ipv6_support:
                return ip
            
            def allowed_gai_family():
                return socket.AF_INET6


        requests.packages.urllib3.util.connection.allowed_gai_family = allowed_gai_family

        ip = requests.get(url, timeout=timeout, verify=not insecure).text.rstrip()
    
        if pattern is not None:
            match = re.search(pattern, ip)
            if match:
                ip = match.group(1)
            
        # valid ip returned ?
        if not checkifvalid.ipv4_address(ip) and not checkifvalid.ipv6_address(ip):
            raise Exception("invalid IP returned: %s", ip)
            return None

    except requests.exceptions.RequestException as e:
        logging.error("[http] - %s" % e)
    return ip

async def _lookup_stun(host, port, family, transport, timeout):
    async with aiostun.Client(host=host, port=port, family=family, proto=transport, timeout=timeout) as stunc:
        mapped_addr = await stunc.get_mapped_address()
    return mapped_addr

def lookup_stun(host, port, ipversion, transport, timeout):
    ip = None
    try:
        if ipversion == constants.IPv4:
            family = aiostun.IP4
        elif ipversion == constants.IPv6:
            family = aiostun.IP6
        else:
            family = aiostun.IP4

        if transport.lower() == "udp":
            transport = aiostun.UDP
        elif transport.lower() == "tcp":
            transport = aiostun.TCP
        elif transport.lower() == "tls":
            transport = aiostun.TLS
        else:
            transport = aiostun.UDP

        mapped_addr = asyncio.run(_lookup_stun(host, port, family, transport, timeout))
        ip = mapped_addr["ip"]

        # valid ip returned ?
        if not checkifvalid.ipv4_address(ip) and not checkifvalid.ipv6_address(ip):
            raise Exception("invalid IP returned: %s", ip)
            return None
        
    except Exception as e:
        logging.error("[stun] - %s" % e)
    return ip

def _resolv_addr(nameservers=[], qname="localhost", rdtype="A", rdclass="IN", timeout=5.0, pattern=None):
    rdtype = rdtype.lower()

    dnsresolv = dns.resolver.Resolver(configure=False)
    dnsresolv.nameservers = nameservers
    dnsresolv.timeout = timeout
    dnsresolv.lifetime = timeout
    
    # make dns resolution and read only the first response
    answers = dnsresolv.resolve(qname, rdtype, rdclass)
    if rdtype == "txt" and len(answers):
        text = []
        for line in answers[0].strings:
            text.append(line.decode())
        if pattern is not None:
            match = re.search(pattern, "\n".join(text))
            if match:
                return match.group(1)
        return "\n".join(text)

    if rdtype in [ "a", "aaaa" ] and len(answers):
        return answers[0].to_text()

    return None

def lookup_dns_v4(nameservers, lookup, qtype, dnsclass, timeout, pattern):
    _qtype = "A" if qtype is None else qtype

    # resolvers nameservers
    resolver = dns.resolver.Resolver()
    _nameservers = []
    for n in nameservers:
        answer = resolver.resolve(n, "A")
        for rdata in answer:
            _nameservers.append(rdata.to_text())

    return lookup_dns(_nameservers, lookup, _qtype, dnsclass, timeout ,pattern)

def lookup_dns_v6(nameservers, lookup, qtype, dnsclass, timeout, pattern):
    _qtype = "AAAA" if qtype is None else qtype

    # resolvers nameservers
    resolver = dns.resolver.Resolver()
    _nameservers = []
    for n in nameservers:
        answer = resolver.resolve(n, "AAAA")
        for rdata in answer:
            _nameservers.append(rdata.to_text())

    return lookup_dns(_nameservers, lookup, _qtype, dnsclass, timeout, pattern)

def lookup_dns(nameservers, lookup, qtype, dnsclass, timeout, pattern):
    ip = None
    try:
        ip = _resolv_addr(nameservers=nameservers, qname=lookup, 
                          rdtype=qtype, rdclass=dnsclass,
                          timeout=timeout, pattern=pattern)
        
        # valid ip returned ?
        if not checkifvalid.ipv4_address(ip) and not checkifvalid.ipv6_address(ip):
            raise Exception("invalid IP returned: %s", ip)
            return None
    except dns.exception.DNSException as e:
        logging.error("[dns] - %s" % e)
    return ip
