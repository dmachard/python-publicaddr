from random import randrange
from publicaddr import constants

_https_providers = []
_dns_providers = []
_stun_providers = []

def set_http_providers(providers):
    global _https_providers
    _https_providers.extend(providers)
    for prov in _https_providers:
        prov["mode"] = constants.HTTPS

def set_dns_providers(providers):
    global _dns_providers
    _dns_providers.extend(providers)
    for prov in _dns_providers:
        prov["mode"] = constants.DNS

def set_stun_providers(providers):
    global _stun_providers
    _stun_providers.extend(providers)
    for prov in _stun_providers:
        prov["mode"] = constants.STUN

def pick_all():
    global _https_providers 

    # merge all providers
    allproviders = []
    allproviders.extend(_https_providers)
    allproviders.extend(_dns_providers)
    allproviders.extend(_stun_providers)

    id = randrange(len(allproviders))
    return allproviders[id]

def pick_https():
    global _https_providers 
    id = randrange(len(_https_providers))
    return _https_providers[id]

def pick_dns():
    global _dns_providers 
    id = randrange(len(_dns_providers))
    return _dns_providers[id]

def pick_stun():
    global _stun_providers 
    id = randrange(len(_stun_providers))
    return _stun_providers[id]