import unittest
import publicaddr

class TestGoogle(unittest.TestCase):
    def test_get_ip4(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.PROVIDER_GOOGLE, ipversion=publicaddr.IP_V4)
        self.assertNotEqual(ip, "")
    def test_get_ip6(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.PROVIDER_GOOGLE, ipversion=publicaddr.IP_V6)
        self.assertNotEqual(ip, "")
    def test_get_all(self):
        """get dns ip6 and ip4"""
        ips = publicaddr.getall(provider=publicaddr.PROVIDER_GOOGLE)
        self.assertIn("ip4", ips)
        self.assertIn("ip6", ips)
