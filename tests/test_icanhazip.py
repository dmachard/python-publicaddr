import unittest
import publicaddr

class TestIcanhazip(unittest.TestCase):
    def test_get_ip4_http(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.ICANHAZIP, ip=publicaddr.IPv4, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")
    def test_get_ip6_http(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.ICANHAZIP, ip=publicaddr.IPv6, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")