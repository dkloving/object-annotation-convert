import unittest
import pandas as pd

from modules.pascalvoc import PascalVOCReader
from utils.summaries import describe_folders


class TestPascalVOC(unittest.TestCase):

    test_folder = 'test_data\\pascalvoc'

    def test_read(self):
        # correctly read and count files while rejecting non-existing images
        reader = PascalVOCReader(label_folder=self.test_folder).fit()
        self.assertEqual(len(reader._invalid_image_refs), 1)
        self.assertEqual(describe_folders(reader._dataframe['image_id'])[-1], '3')
        # correctly read and count files without rejection of non-existing images
        reader = PascalVOCReader(label_folder=self.test_folder, include_missing_images=True).fit()
        self.assertEqual(len(reader._invalid_image_refs), 0)
        self.assertEqual(describe_folders(reader._dataframe['image_id'])[-1], '4')

