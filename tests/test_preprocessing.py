import unittest

from processing.preprocessing import preprocess_rate, preprocess_weather


class TestPreprocessing(unittest.TestCase):
    def test_warm_clothes_when_temperature_below_zero(self):
        result = preprocess_weather(
            {
                "temp_c": -5.0,
                "description": "snow",
            }
        )

        self.assertTrue(result["warm_clothes"])

    def test_no_warm_clothes_when_temperature_above_zero(self):
        result = preprocess_weather(
            {
                "temp_c": 10.0,
                "description": "clear sky",
            }
        )

        self.assertFalse(result["warm_clothes"])

    def test_expensive_when_rate_above_100(self):
        result = preprocess_rate(
            {
                "currency": "USD",
                "rate_to_rub": 120.0,
            }
        )

        self.assertTrue(result["expensive"])

    def test_no_expensive_when_rate_below_100(self):
        result = preprocess_rate(
            {
                "currency": "USD",
                "rate_to_rub": 80.0,
            }
        )

        self.assertFalse(result["expensive"])


if __name__ == "__main__":
    unittest.main()
