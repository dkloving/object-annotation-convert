import unittest
import pandas as pd

from modules.pascalvoc import PascalVOCReader
from utils.summaries import describe_folders


class TestPascalVOC(unittest.TestCase):

    test_folder_labels = 'test_data\\pascalvoc_labels'
    test_folder_images = 'test_data\\jpeg_images'

    def test_read(self):
        # correctly read and count files while rejecting non-existing images
        reader = PascalVOCReader(label_folder=self.test_folder_labels).fit()
        self.assertEqual(len(reader._invalid_image_refs), 4)
        # correctly read and count files with overridden image folder
        reader = PascalVOCReader(label_folder=self.test_folder_labels, image_folder_override=self.test_folder_images).fit()
        self.assertEqual(describe_folders(reader._dataframe['image_id'])[-1], '4')
        # correctly read and count files without rejection of non-existing images
        reader = PascalVOCReader(label_folder=self.test_folder_labels, include_missing_images=True).fit()
        self.assertEqual(len(reader._invalid_image_refs), 0)
        self.assertEqual(describe_folders(reader._dataframe['image_id'])[-1], '4')

