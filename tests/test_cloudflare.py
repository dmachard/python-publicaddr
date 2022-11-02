import unittest
import publicaddr
class TestCloudflare(unittest.TestCase):
    def test_get_ip4_dns(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.CLOUDFLARE, ip=publicaddr.IPv4)
        self.assertNotEqual(ip, "")
    def test_get_ip6_dns(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.CLOUDFLARE, ip=publicaddr.IPv6)
        self.assertNotEqual(ip, "")
    def test_get_ip4_http(self):
        """get http ip4"""
        ip = publicaddr.get(provider=publicaddr.CLOUDFLARE, ip=publicaddr.IPv4, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")
    def test_get_ip6_http(self):
        """get http ip6"""
        ip = publicaddr.get(provider=publicaddr.CLOUDFLARE, ip=publicaddr.IPv6, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")
