from random import randrange

_providers = []
_providers_dns = []
_providers_http = []
_providers_stuns = []

def set_providers(providers):
    """set all providers"""
    global _providers
    global _providers_dns
    global _providers_http
    global _providers_stuns
    _providers = providers

    for prov in providers:
        if len(prov.dns_servers): _providers_dns.append(prov)
        if len(prov.http_servers): _providers_http.append(prov)
        if len(prov.stuns_servers): _providers_stuns.append(prov)

def pick_proto():
    return randrange(3)+1

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

def pick_stuns():
    global _providers_stuns
    id = randrange(len(_providers_stuns))
    return _providers_stuns[id]
