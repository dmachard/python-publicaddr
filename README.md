![Testing](https://github.com/dmachard/python-publicaddr/workflows/Testing/badge.svg) ![Build](https://github.com/dmachard/python-publicaddr/workflows/Build/badge.svg) ![Publish](https://github.com/dmachard/python-publicaddr/workflows/Publish/badge.svg)

# What is this?

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Simple python module for getting your **public IP V4 and V6** from several providers in **random** mode with also several protocols (DNS, HTTPS and STUN).

Supported providers

| IP Checker   | HTTPS | STUN | DNS | IPv4 | IPv6 | Use Policy                                     |
|--------------|-------|------|-----|------|------|------------------------------------------------|
| google       |  ❌   |   ✔️  |  ✔️  |  ✔️   |  ✔️   |                                                |
| cloudflare   |  ✔️    |  ❌  |  ✔️  |  ✔️   |  ✔️   |                                                |
| openDNS      |  ❌   |  ❌  |  ✔️  |  ✔️   |  ✔️   |                                                |
| akamai       |  ✔️    |  ❌  |  ✔️  |  ✔️   |  ✔️   |                                                |
| ipify        |  ✔️    |  ❌  |  ❌ |  ✔️   |  ✔️   |                                                |
| icanhazip    |  ✔️    |  ❌  |  ❌ |  ✔️   |  ✔️   |                                                |
| matrix       |  ❌   |  ✔️   |  ❌ |  ✔️   |  ✔️   |                                                |
| framasoft    |  ❌   |  ✔️   |  ❌ |  ✔️   |  ✔️   |                                                |
| ifconfig.me  |  ✔️   |  ❌   |  ❌ |  ✔️   |  ✔️   |                                                |

## Installation

![python 3.13.x](https://img.shields.io/badge/python%203.13.x-tested-blue) ![python 3.12.x](https://img.shields.io/badge/python%203.12.x-tested-blue) ![python 3.11.x](https://img.shields.io/badge/python%203.11.x-tested-blue) ![python 3.10.x](https://img.shields.io/badge/python%203.10.x-tested-blue)

This module can be installed from [pypi](https://pypi.org/project/publicaddr/) website

```bash
pip install publicaddr
```

## Lookup for IPv4 and IPv6

Lookup for your public IPs from random providers with DNS or HTTP protocols with 3 retries if no ips are returned.
This is the default behaviour of the `lookup` function.

```python
import publicaddr

publicaddr.lookup()
{'ip4': 'x.x.x.x', 'ip6': 'x:x:x:x:x:x:x:x', 'provider': 'opendns',
'proto': 'dns', 'duration': '0.037'}
```

## Configuration

This module can be configurated with environment variables
| Variables | Description |
| ------------- | ------------- |
| PUBLICADDR_DEBUG | debug mode 1 or 0 |
| PUBLICADDR_TIMEOUT | timeout, default is 2s |
| PUBLICADDR_RETRIES | retries, default is 3|
| PUBLICADDR_IPV6_ENABLED | enable ipv6 with 1 or 0 to disable |
| PUBLICADDR_LOOKUP_HTTPS | lookup with HTTPS protocol  (1 or 0 to disable) |
| PUBLICADDR_LOOKUP_DNS | lookup with DNS protocol  (1 or 0 to disable) |
| PUBLICADDR_LOOKUP_STUN | lookup with STUN protocol  (1 or 0 to disable) |


## Specific lookups

### Lookup for public IP with specific protocol

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

### Get IPv4 or IPv6 only

Get your public IPv4 with default provider (Google with DNS protocol).

```python
import publicaddr

publicaddr.get(ip=publicaddr.IPv4)
{'ip': 'x.x.x.x', 'duration': '0.025'}
```

Default constants for IP version:

- `publicaddr.IPv4`
- `publicaddr.IPv6`

### Get IP with specific provider

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
- `publicaddr.IFCONFIG_ME`

## For developpers

### Run from source

```bash
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```

```bash
python3 -m pip install -r requirements.txt
python3 example.py
```

### Custom configuration

See the default [configuration file](../main/publicaddr/publicaddr.yml)

### Run test units

```bash
python3 -m unittest discover tests/
```
