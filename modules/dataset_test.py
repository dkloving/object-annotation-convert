import unittest
import pandas as pd
from modules.dataset import Dataset


class TestDataset(unittest.TestCase):

    test_data = [{'image_id': 'test0.jpg',
                  'image_width':100,
                  'image_height': 60,
                  'image_depth': 3,
                  'x_min': 10,
                  'x_max': 50,
                  'y_min': 20,
                  'y_max':50,
                  'class_id': 0,
                  'class_name': 'cat'},
                 {'image_id': 'test1.jpg',
                  'image_width': 200,
                  'image_height': 160,
                  'image_depth': 3,
                  'x_min': 20,
                  'x_max': 150,
                  'y_min': 30,
                  'y_max': 80,
                  'class_id': 1,
                  'class_name': 'dog'},
                 {'image_id': 'test2.jpg',
                  'image_width': 1024,
                  'image_height': 768,
                  'image_depth': 3,
                  'x_min': 300,
                  'x_max': 640,
                  'y_min': 320,
                  'y_max': 972,
                  'class_id': 42,
                  'class_name': 'platypus'}
                 ]

    def test_init(self):
        # construction from dataframe
        self.failureException(Dataset(pd.DataFrame(self.test_data)))
        # construction with legitimate non-dataframe
        self.failureException(Dataset(self.test_data))
        # construction with missing columns
        with self.failUnlessRaises(AttributeError):
            _ = Dataset(pd.DataFrame(self.test_data).drop(['x_min'], axis=1))
        # construction with invalid non-dataframe
        with self.failUnlessRaises(AttributeError):
            _ = Dataset((4, 5, 6))
        # calculate length of single dataset
        self.assertEqual(len(Dataset(pd.DataFrame(self.test_data))), len(self.test_data))
        # add two Dataset objects and construct with list
        object_a = Dataset(pd.DataFrame(self.test_data))
        object_b = Dataset(pd.DataFrame(self.test_data))
        self.assertEqual(len(object_a + object_b), 2*len(self.test_data))
        self.assertEqual(len(Dataset([object_a, object_b])), 2*len(self.test_data))
        # read out of bounds
        with self.failUnlessRaises(IndexError):
            Dataset(pd.DataFrame(self.test_data)).read(3)
        # read() and generator functionality
        test_iterable = Dataset(pd.DataFrame(self.test_data))
        self.assertEqual([item for item in test_iterable],
                         [(item, item['image_id']) for item in self.test_data])
