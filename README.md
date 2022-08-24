# Intro

![Testing](https://github.com/dmachard/python-publicaddr/workflows/Testing/badge.svg) ![Build](https://github.com/dmachard/python-publicaddr/workflows/Build/badge.svg) ![Publish](https://github.com/dmachard/python-publicaddr/workflows/Publish%20to%20PyPI/badge.svg) 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/publicaddr)

Simple python module for getting your public IP V4 and V6 with several providers support.
The following one are supported:
- Google (DNS)
- Cloudflare (DNS)
- OpenDNS (DNS)
- Akamai (HTTP)

## Installation

This module can be installed from [pypi](https://pypi.org/project/python_publicaddr/) website

```bash
pip install publicaddr
```

## Usage

```python
import publicaddr

publicaddr.getall()
{'ip4': 'x.x.x.x', 'ip6': 'x:x:x:x:x:x:x:x'}
```

## Provider

```python
import publicaddr
from publicaddr import PROVIDER_GOOGLE, PROVIDER_OPENDNS, PROVIDER_CLOUDFLARE, PROVIDER_AKAMAI

publicaddr.getall(PROVIDER_AKAMAI)
{'ip4': 'x.x.x.x', 'ip6': 'x:x:x:x:x:x:x:x'}
```

## For developpers

Run test units

```bash
python3 -m unittest -v discover tests/
```