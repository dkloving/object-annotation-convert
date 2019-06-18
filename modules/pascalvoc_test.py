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
        self.assertEqual(len(reader._get_invalid_images()), 4)
        # correctly read and count files with overridden image folder
        reader = PascalVOCReader(label_folder=self.test_folder_labels,
                                 image_folder_override=self.test_folder_images).fit()
        self.assertEqual(describe_folders(reader._dataframe['image_id'])[-1], '4')
        self.assertEqual(len(reader._get_invalid_images()), 0)
        # test make dataset produces dataset with all entries
        dataset = reader.make_dataset()
        self.assertEqual(len(dataset), len(reader._dataframe))
