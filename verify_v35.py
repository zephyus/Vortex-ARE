import unittest
from unittest.mock import patch, MagicMock
from system_engine import SystemEngine

class TestAdaptiveMetabolism(unittest.TestCase):
    def setUp(self):
        self.engine = SystemEngine()
        self.engine.config["personality"] = "Default" # Base = 4.0
        self.engine.config["metabolic_interval"] = 4.0

    @patch('psutil.cpu_percent')
    def test_cpu_throttling(self, mock_cpu):
        print("Testing CPU Throttling (High Load -> Slow Down)...")
        mock_cpu.return_value = 90.0
        # Mock health check to 0 issues
        self.engine.check_code_health = MagicMock(return_value=[])
        
        interval = self.engine.calculate_adaptive_heartbeat()
        # Base 4.0 * 2.0 (CPU > 80) = 8.0
        self.assertEqual(interval, 8.0)
        print(f"SUCCESS: Interval scaled to {interval}m under 90% CPU.")

    @patch('psutil.cpu_percent')
    def test_cpu_acceleration(self, mock_cpu):
        print("Testing CPU Acceleration (Low Load -> Speed Up)...")
        mock_cpu.return_value = 10.0
        self.engine.check_code_health = MagicMock(return_value=[])
        
        interval = self.engine.calculate_adaptive_heartbeat()
        # Base 4.0 * 0.8 (CPU < 20) = 3.2
        self.assertEqual(interval, 3.2)
        print(f"SUCCESS: Interval scaled to {interval}m under 10% CPU.")

    @patch('psutil.cpu_percent')
    def test_error_throttling(self, mock_cpu):
        print("Testing Error Throttling (High Errors -> Slow Down)...")
        mock_cpu.return_value = 30.0 # Nominal
        # Mock 6 issues
        self.engine.check_code_health = MagicMock(return_value=[1,2,3,4,5,6])
        
        interval = self.engine.calculate_adaptive_heartbeat()
        # Base 4.0 * 1.5 (Errors > 5) = 6.0
        self.assertEqual(interval, 6.0)
        print(f"SUCCESS: Interval scaled to {interval}m with 6 issues.")

if __name__ == "__main__":
    unittest.main()
