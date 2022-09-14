import unittest
import publicaddr
class TestCloudflare(unittest.TestCase):
    def test_get_ip4(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.CLOUDFLARE, ip=publicaddr.IPv4)
        self.assertNotEqual(ip, "")
    def test_get_ip6(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.CLOUDFLARE, ip=publicaddr.IPv6)
        self.assertNotEqual(ip, "")