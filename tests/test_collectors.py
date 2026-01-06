import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from script_info.collectors import (
    get_basic_info,
    get_hardware_info,
    get_storage_info,
    get_network_info,
    get_software_info,
    get_security_info
)

class TestCollectors(unittest.TestCase):
    def test_basic_info(self):
        info = get_basic_info()
        self.assertIsInstance(info, dict)
        self.assertIn('OS Name', info)

    def test_hardware_info(self):
        info = get_hardware_info()
        self.assertIsInstance(info, dict)
        # Check for at least one expected key (CPU)
        keys = info.keys()
        self.assertTrue(any('CPU' in k for k in keys))

    def test_storage_info(self):
        info = get_storage_info()
        self.assertIsInstance(info, dict)

    def test_network_info(self):
        info = get_network_info()
        self.assertIsInstance(info, dict)
        self.assertIn('Hostname', info)

    def test_software_info(self):
        info = get_software_info()
        self.assertIsInstance(info, dict)
        self.assertIn('Python Version', info)
        
    def test_security_info(self):
        info = get_security_info()
        self.assertIsInstance(info, dict)

if __name__ == '__main__':
    unittest.main()
