import unittest
import publicaddr
import ipaddress

class TestLookup(unittest.TestCase):
    
    def is_valid_ip(self, ip, version):
        """Helper to validate if the given IP is valid for the specified version (IPv4 or IPv6)."""
        try:
            if version == publicaddr.IPv4 and ip is not None:
                ipaddress.IPv4Address(ip)
            elif version == publicaddr.IPv6 and ip is not None:
                ipaddress.IPv6Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    def test_lookup(self):
        """Test DNS lookup for both IPv4 and IPv6."""
        yourIPs = publicaddr.lookup()
        
        self.assertIn("ip4", yourIPs, "Expected 'ip4' key in the response")
        if yourIPs["ip4"]:
            self.assertTrue(self.is_valid_ip(yourIPs["ip4"], publicaddr.IPv4), f"Invalid IPv4 address: {yourIPs['ip4']}")
        
        self.assertIn("ip6", yourIPs, "Expected 'ip6' key in the response")
        if yourIPs["ip6"]:
            self.assertTrue(self.is_valid_ip(yourIPs["ip6"], publicaddr.IPv6), f"Invalid IPv6 address: {yourIPs['ip6']}")
