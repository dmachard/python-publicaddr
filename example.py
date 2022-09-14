import publicaddr

myip = publicaddr.lookup()
print(myip)

myip = publicaddr.get(provider=publicaddr.AKAMAI, proto=publicaddr.HTTPS, ip=publicaddr.IPv4)

print(myip)