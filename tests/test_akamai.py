import unittest
import publicaddr
import urllib3
import os
import ipaddress

urllib3.disable_warnings()

class TestAkamai(unittest.TestCase):
    
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

    def test_get_dns_ip4(self):
        """Test DNS retrieval for IPv4."""
        ret = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv4)
        self.assertIsNotNone(ret, "Expected a non-null response for IPv4 DNS request")
        self.assertIn("ip", ret, "Expected 'ip' key in the response dictionary for IPv4")
        self.assertNotEqual(ret["ip"], "", "IPv4 address should not be an empty string")
        self.assertTrue(self.is_valid_ip(ret["ip"], publicaddr.IPv4), f"Invalid IPv4 address: {ret['ip']}")

    def test_get_dns_ip6(self):
        """Test DNS retrieval for IPv6"""
        ipv6_enabled = os.getenv('PUBLICADDR_IPV6_ENABLED')
        
        if ipv6_enabled is not None and not bool(int(ipv6_enabled)):
            self.skipTest("IPv6 is disabled via environment variable")
        
        ret = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv6)
        self.assertIsNotNone(ret, "Expected a non-null response for IPv6 DNS request")
        self.assertIn("ip", ret, "Expected 'ip' key in the response dictionary for IPv6")
        self.assertNotEqual(ret["ip"], "", "IPv6 address should not be an empty string")
        self.assertTrue(self.is_valid_ip(ret["ip"], publicaddr.IPv6), f"Invalid IPv6 address: {ret['ip']}")

    def test_get_ip4_http(self):
        """Test HTTP retrieval for IPv4."""
        ret = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv4, proto=publicaddr.HTTPS)
        self.assertIsNotNone(ret, "Expected a non-null response for IPv4 HTTP request")
        self.assertIn("ip", ret, "Expected 'ip' key in the response dictionary for IPv4")
        self.assertNotEqual(ret["ip"], "", "IPv4 address should not be an empty string")
        self.assertTrue(self.is_valid_ip(ret["ip"], publicaddr.IPv4), f"Invalid IPv4 address: {ret['ip']}")

    def test_get_ip6_http(self):
        """Test HTTP retrieval for IPv6"""
        ipv6_enabled = os.getenv('PUBLICADDR_IPV6_ENABLED')
        
        if ipv6_enabled is not None and not bool(int(ipv6_enabled)):
            self.skipTest("IPv6 is disabled via environment variable")
        
        ret = publicaddr.get(provider=publicaddr.AKAMAI, ip=publicaddr.IPv6, proto=publicaddr.HTTPS)
        self.assertIsNotNone(ret, "Expected a non-null response for IPv6 HTTP request")
        self.assertIn("ip", ret, "Expected 'ip' key in the response dictionary for IPv6")
        self.assertNotEqual(ret["ip"], "", "IPv6 address should not be an empty string")
        self.assertTrue(self.is_valid_ip(ret["ip"], publicaddr.IPv6), f"Invalid IPv6 address: {ret['ip']}")
