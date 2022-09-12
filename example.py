import publicaddr

externalip = publicaddr.lookup(providers=publicaddr.STUNS_PROVIDERS, retries=1)
print(externalip)