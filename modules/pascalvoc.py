import os
import glob
from lxml import etree
import pandas as pd
from pathlib import PurePath
from warnings import warn

from modules.dataset import Dataset
from utils.io import read_image_file


class PascalVOCReader:
    """TODO: docstring"""

    def __init__(self, label_folder, image_folder_override=None):
        """ TODO: docstring"""
        if not os.path.isdir(label_folder):
            raise ValueError('Label folder {} not a valid directory'.format(label_folder))
        if image_folder_override is not None:
            if not os.path.isdir(label_folder):
                raise ValueError('Label folder {} not a valid directory'.format(label_folder))
        self._image_folder_override = image_folder_override
        self._label_folder = label_folder
        self._dataframe = pd.DataFrame()
        self._class_ids = dict()

    def make_dataset(self, include_invalid_images=False):
        source_dataframe = self._dataframe.drop('image_valid', axis=1) if include_invalid_images else\
            self._dataframe[self._dataframe.image_valid].drop('image_valid', axis=1)
        dataset = Dataset(source_object=source_dataframe, image_read_method=read_image_file)
        return dataset

    def fit(self, deep_validate_images=False):
        """TODO: docstring"""
        if deep_validate_images:
            warn("Deep validation of images can be very slow on large datasets.")
        label_files = glob.glob(os.path.join(self._label_folder, '*.xml'))
        objects_df = pd.DataFrame()
        for label_file in label_files:
            with open(label_file, 'r') as file:
                xml = etree.fromstring(file.read())
                new_df = self.__xml_to_dataframe(xml, deep_validate_images)
                objects_df = pd.concat([objects_df, new_df])
        self._dataframe = objects_df
        return self

    def read(self):
        pass

    def __validate_image(self, image_path, deep, width, height, depth):
        if deep:
            raise NotImplementedError
        else:
            return os.path.isfile(image_path)

    def __xml_to_dataframe(self, xml, deep_validate_images):
        """ TODO: docstring"""
        if self._image_folder_override is None:
            image_id = str(PurePath(xml.find('path').text))  # PurePath handles POSIX / Win32 differences
        else:
            image_id = str(PurePath(self._image_folder_override).joinpath(PurePath(xml.find('filename').text)))
        image_width = xml.find('size').find('width').text
        image_height = xml.find('size').find('height').text
        image_depth = xml.find('size').find('depth').text
        image_valid = self.__validate_image(image_id, deep_validate_images, image_width, image_height, image_depth)
        objects = []
        for item in xml:
            if item.tag == 'object':
                class_name = item.find('name').text
                if class_name not in self._class_ids:
                    self._class_ids[class_name] = len(self._class_ids)
                class_id = self._class_ids[class_name]
                objects.append({'class_name': class_name,
                                'class_id': class_id,
                                'x_min': item.find('bndbox').find('xmin').text,
                                'x_max': item.find('bndbox').find('xmax').text,
                                'y_min': item.find('bndbox').find('ymin').text,
                                'y_max': item.find('bndbox').find('ymax').text
                                })
        objects = pd.DataFrame(objects)
        for item in ['image_id', 'image_width', 'image_height', 'image_depth', 'image_valid']:
            objects[item] = eval(item)
        return objects

    def _get_invalid_images(self):
        return self._dataframe[~self._dataframe.image_valid].image_id.unique()


class PascalVOCWriter:

    def __init__(self):
        raise NotImplementedError
