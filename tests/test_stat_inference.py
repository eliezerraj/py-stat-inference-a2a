import unittest

from domain.service.inference_stat import compute_stat
from infrastructure.adapter.handler import handler_compute_stat
from shared.exception.exceptions import A2ARequestError


class StatInferenceTests(unittest.TestCase):
    def test_single_value_metrics_are_finite(self):
        result = compute_stat([10.0])

        self.assertEqual(result.mean, 10.0)
        self.assertEqual(result.std, 0.0)
        self.assertEqual(result.fano_factor, 0.0)
        self.assertEqual(result.mad, 0.0)
        self.assertEqual(result.n_slope, 0.0)
        self.assertEqual(result.autocorr, 0.0)

    def test_mad_uses_median_absolute_deviation(self):
        result = compute_stat([8, 8, 8, 8, 12])

        self.assertEqual(result.mad, 0.0)

    def test_handler_rejects_empty_payload(self):
        with self.assertRaises(A2ARequestError):
            handler_compute_stat({})

    def test_handler_rejects_non_finite_values(self):
        with self.assertRaises(A2ARequestError):
            handler_compute_stat({"data": [1.0, float("nan")]})


if __name__ == "__main__":
    unittest.main()