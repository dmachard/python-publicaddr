import unittest
import publicaddr

class TestLookup(unittest.TestCase):
    def test_lookup(self):
        """get dns ip6 and ip4"""
        ips = publicaddr.lookup()
        self.assertIn("ip4", ips)
        self.assertIn("ip6", ips)
