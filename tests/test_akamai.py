import unittest
import publicaddr

class TestAkamai(unittest.TestCase):
    def test_get_dns_ip4(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.PROVIDER_AKAMAI, ipversion=publicaddr.IP_V4)
        self.assertNotEqual(ip, "")
    def test_get_dns_ip6(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.PROVIDER_AKAMAI, ipversion=publicaddr.IP_V6)
        self.assertNotEqual(ip, "")
    def test_get_ip4_http(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.PROVIDER_AKAMAI, ipversion=publicaddr.IP_V4, ipproto=publicaddr.PROTO_HTTP)
        self.assertNotEqual(ip, "")
    def test_get_ip6_http(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.PROVIDER_AKAMAI, ipversion=publicaddr.IP_V6, ipproto=publicaddr.PROTO_HTTP)
        self.assertNotEqual(ip, "")
    def test_lookup(self):
        """get dns ip6 and ip4"""
        ips = publicaddr.lookup()
        self.assertIn("ip4", ips)
        self.assertIn("ip6", ips)
