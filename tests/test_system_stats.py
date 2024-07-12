import unittest
from src.system_stats import get_temperature, get_power_consumption


class TestSystemStats(unittest.TestCase):
    def test_get_temperature(self):
        """Test to ensure temperature retrieval outputs expected format."""
        temp_output = get_temperature()
        # Assuming temperature should be a string containing at least one numeric value
        self.assertTrue(any(char.isdigit() for char in temp_output), "Temperature output should contain digits.")

    def test_get_power_consumption(self):
        """Test to ensure power consumption retrieval outputs expected format or error message."""
        power_output = get_power_consumption()
        # Test for expected output format or a not available message
        self.assertTrue("W" in power_output or "not available" in power_output,
                        "Power output should contain 'W' for watts or 'not available'.")


if __name__ == '__main__':
    unittest.main()
