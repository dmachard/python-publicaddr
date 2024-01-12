import publicaddr

myip = publicaddr.get(provider=publicaddr.CLOUDFLARE, proto=publicaddr.HTTPS, ip=publicaddr.IPv4)
print(myip)

myip = publicaddr.lookup(providers=publicaddr.HTTPS)
print(myip)

myip = publicaddr.get(provider=publicaddr.AKAMAI, proto=publicaddr.HTTPS, ip=publicaddr.IPv4)
print(myip)

myip = publicaddr.get(provider=publicaddr.GOOGLE, proto=publicaddr.STUN, ip=publicaddr.IPv4)
print(myip)