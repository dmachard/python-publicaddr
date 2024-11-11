import unittest
import publicaddr
import os
import ipaddress

class TestMatrix(unittest.TestCase):
    def is_valid_ip(self, ip, version):
        """Helper to validate if the given IP is valid for the specified version (IPv4 or IPv6)."""
        try:
            if version == publicaddr.IPv4:
                ipaddress.IPv4Address(ip)
            elif version == publicaddr.IPv6:
                ipaddress.IPv6Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    def test_get_ip4_stun(self):
        """Test STUN retrieval for IPv4."""
        ret = publicaddr.get(provider=publicaddr.MATRIX, proto=publicaddr.STUN, ip=publicaddr.IPv4)
        self.assertIsNotNone(ret, "Expected a non-null response")
        self.assertIn("ip", ret, "Expected 'ip' key in the response dictionary for IPv4")
        self.assertNotEqual(ret["ip"], "", "IPv4 address should not be an empty string")
        self.assertTrue(self.is_valid_ip(ret["ip"], publicaddr.IPv4), f"Invalid IPv4 address: {ret['ip']}")

    def test_get_ip6_stun(self):
        """Test STUN retrieval for IPv6"""
        ipv6_enabled = os.getenv('PUBLICADDR_IPV6_ENABLED')
        
        # Skip the test if IPv6 is explicitly disabled via environment variable
        if ipv6_enabled is not None and not bool(int(ipv6_enabled)):
            self.skipTest("IPv6 is disabled via environment variable")
        
        ret = publicaddr.get(provider=publicaddr.MATRIX, proto=publicaddr.STUN, ip=publicaddr.IPv6)
        self.assertIsNotNone(ret, "Expected a non-null response")
        self.assertIn("ip", ret, "Expected 'ip' key in the response dictionary for IPv6")
        self.assertNotEqual(ret["ip"], "", "IPv6 address should not be an empty string")
        self.assertTrue(self.is_valid_ip(ret["ip"], publicaddr.IPv6), f"Invalid IPv6 address: {ret['ip']}")