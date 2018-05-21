import unittest
import numpy as np

from create_test_model import create_test_model

import sys
sys.path.append("..")

from FeedForwardNetAsync import FeedForwardNetAsync

class TestFeedForwardNetAsync(unittest.TestCase):

    def test_shape_binary(self):
        model = lambda: create_test_model(10, 1)
        model = FeedForwardNetAsync(model)
        model.predict_on_batch(np.ones((1, 10)))
        pred = model.collect()
        self.assertEqual(pred.shape, (1, 1))

    def test_shape_binary_multiple(self):
        model = lambda: create_test_model(10, 1)
        model = FeedForwardNetAsync(model)
        model.predict_on_batch(np.ones((10, 10)))
        pred = model.collect()
        self.assertEqual(pred.shape, (10, 1))
        
    def test_shape_multilabel(self):
        model = lambda: create_test_model(10, 10)
        model = FeedForwardNetAsync(model)
        model.predict_on_batch(np.ones((1, 10)))
        pred = model.collect()
        self.assertEqual(pred.shape, (1, 10))

    def test_shape_multilabel_multiple(self):
        model = lambda: create_test_model(10, 10)
        model = FeedForwardNetAsync(model)
        model.predict_on_batch(np.ones((10, 10)))
        pred = model.collect()
        self.assertEqual(pred.shape, (10, 10))


if __name__ == '__main__':
    unittest.main()