from random import randrange

_providers = []
_providers_dns = []
_providers_http = []

def set_providers(providers):
    """set all providers"""
    global _providers
    global _providers_dns
    global _providers_http
    _providers = providers

    for prov in providers:
        if len(prov.dns_servers): _providers_dns.append(prov)
        if len(prov.http_servers): _providers_http.append(prov)

def pick_proto():
    return randrange(2)+1

def pick_all():
    global _providers 
    id = randrange(len(_providers))
    return _providers[id]

def pick_dns():
    global _providers_dns
    id = randrange(len(_providers_dns))
    return _providers_dns[id]

def pick_http():
    global _providers_http
    id = randrange(len(_providers_http))
    return _providers_http[id]
