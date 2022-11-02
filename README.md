# What is this?

![Testing](https://github.com/dmachard/python-publicaddr/workflows/Testing/badge.svg) ![Build](https://github.com/dmachard/python-publicaddr/workflows/Build/badge.svg) ![Publish](https://github.com/dmachard/python-publicaddr/workflows/Publish/badge.svg) 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/publicaddr)

Simple python module for getting your **public IP V4 and V6** from several providers in **random** mode with also several protocols (DNS, HTTPS and STUN).

Supported providers:
- [x] Google (DNS & HTTP & STUN)
- [x] Cloudflare (DNS & HTTP)
- [x] OpenDNS (DNS)
- [x] Akamai (DNS & HTTP)
- [x] [Ipify](https://www.ipify.org/) (HTTP)
- [x] Icanhazip (HTTP)
- [x] [Matrix](https://www.matrix.org) (STUN)
- [x] [Framasoft](https://framasoft.org/) (STUN)

## Installation

This module can be installed from [pypi](https://pypi.org/project/publicaddr/) website

```bash
pip install publicaddr
```

## Lookup for IPv4 and v6

Lookup for your public IPs from random providers with DNS or HTTP protocols with 3 retries if no ips are returned.
This is the default behaviour of the `lookup` function.

```python
import publicaddr

publicaddr.lookup()
{'ip4': 'x.x.x.x', 'ip6': 'x:x:x:x:x:x:x:x', 'provider': 'opendns',
'proto': 'dns', 'duration': '0.037'}
```

## Lookup for public IP with specific protocol

Lookup for your public IPs from random DNS providers with specific protocol.

```python
import publicaddr

publicaddr.lookup(providers=publicaddr.DNS, retries=2)
{'ip4': 'x.x.x.x', 'ip6': 'x:x:x:x:x:x:x:x', 'provider': 'opendns',
'proto': 'dns', 'duration': '0.037'}
```

Default constants for transport protocol:
- `publicaddr.HTTPS`
- `publicaddr.DNS`
- `publicaddr.STUN`

## Get IPv4 or IPv6 only

Get your public IPv4 with default provider (Google with DNS protocol).

```python
import publicaddr

publicaddr.get(ip=publicaddr.IPv4)
{'ip': 'x.x.x.x', 'duration': '0.025'}
```

Default constants for IP version:
- `publicaddr.IPv4`
- `publicaddr.IPv6`

## Get IP with specific provider

Example to use the provider Cloudflare instead of the default one.

```python
import publicaddr

myip = publicaddr.get(provider=publicaddr.CLOUDFLARE, proto=publicaddr.DNS)
{'ip': 'x:x:x:x:x:x:x:x', 'duration': '0.020'}
```

Default constants for providers:
- `publicaddr.CLOUDFLARE`
- `publicaddr.GOOGLE`
- `publicaddr.OPENDNS`
- `publicaddr.AKAMAI`
- `publicaddr.IPIFY`
- `publicaddr.ICANHAZIP`
- `publicaddr.MATRIX`
- `publicaddr.FRAMASOFT`

## Custom configuration

See the default [configuration file](../main/publicaddr/publicaddr.yml)

## For developpers

Run test units

```bash
python3 -m unittest discover tests/
```
