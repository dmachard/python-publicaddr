import unittest
import publicaddr
import urllib3
urllib3.disable_warnings()

class TestAkamai(unittest.TestCase):
    def test_get_dns_ip4(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv4)
        self.assertNotEqual(ip, "")
    def test_get_dns_ip6(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv6)
        self.assertNotEqual(ip, "")
    def test_get_ip4_http(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv4, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")
    def test_get_ip6_http(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv6, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")
