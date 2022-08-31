# Intro

![Testing](https://github.com/dmachard/python-publicaddr/workflows/Testing/badge.svg) ![Build](https://github.com/dmachard/python-publicaddr/workflows/Build/badge.svg) ![Publish](https://github.com/dmachard/python-publicaddr/workflows/Publish/badge.svg) 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/publicaddr)

Simple python module for getting your **public IP V4 and V6** from several providers in **random** mode.

Supported providers:
- Google (DNS & HTTP)
- Cloudflare (DNS)
- OpenDNS (DNS)
- Akamai (DNS & HTTP)
- Ipify (HTTP)
- Icanhazip (HTTP)

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
{'ip4': 'x.x.x.x', 'ip6': 'x:x:x:x:x:x:x:x', 'provider': 'OpenDNS',
'proto': 'DNS', 'duration': '0.037'}
```

## Lookup for IPv4 and v6 with DNS protocol only


Lookup for your public IPs from random DNS providers only.

```python
import publicaddr

publicaddr.lookup(providers=DNS_PROVIDERS, retries=2)
{'ip4': 'x.x.x.x', 'ip6': 'x:x:x:x:x:x:x:x', 'provider': 'OpenDNS',
'proto': 'DNS', 'duration': '0.037'}
```

## Get IPv4 only

Get your public IPv4 with default provider (Google with DNS protocol).

```python
import publicaddr

publicaddr.get(ipversion=4)
{'ip': 'x.x.x.x', 'duration': '0.025'}
```

## Get IPv6 only

Get your public IPv6 with default provider (Google with DNS protocol).

```python
import publicaddr

publicaddr.get(ipversion=6)
{'ip': 'x:x:x:x:x:x:x:x', 'duration': '0.063'}
```

## Get IP with specific provider

Example to use the provider Cloudflare instead of the default one.

```python
from publicaddr import get, PROVIDER_CLOUDFLARE, IP_V6, PROTO_DNS

myip = get(provider=PROVIDER_CLOUDFLARE, ipversion=IP_V6, ipproto=PROTO_DNS)
{'ip': 'x:x:x:x:x:x:x:x', 'duration': '0.020'}
```

## For developpers

Run test units

```bash
python3 -m unittest -v discover tests/
```