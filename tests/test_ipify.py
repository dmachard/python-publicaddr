import unittest
import publicaddr


class TestIpify(unittest.TestCase):
    def test_get_ip4_http(self):
        """get dns ip4"""
        ip = publicaddr.get(provider=publicaddr.IPIFY, ip=publicaddr.IPv4, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")
    def test_get_ip6_http(self):
        """get dns ip6"""
        ip = publicaddr.get(provider=publicaddr.IPIFY, ip=publicaddr.IPv6, proto=publicaddr.HTTPS)
        self.assertNotEqual(ip, "")
