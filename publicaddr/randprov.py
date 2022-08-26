from random import randrange

_providers = []

def set_providers(providers):
    """set all providers"""
    global _providers 
    _providers = providers

def pickone():
    global _providers 

    # pick provider
    id = randrange(len(_providers))
    
    # return
    return _providers[id]