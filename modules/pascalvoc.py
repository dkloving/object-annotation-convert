import os
import glob
from lxml import etree
import pandas as pd
from pathlib import PurePath
from warnings import warn

from utils.io import read_image_file


class PascalVOCReader:
    """TODO: docstring"""

    def __init__(self, label_folder, image_folder_override=None, include_missing_images=False):
        """ TODO: docstring"""
        if not os.path.isdir(label_folder):
            raise ValueError('Label folder {} not a valid directory'.format(label_folder))
        if image_folder_override is not None:
            if not os.path.isdir(label_folder):
                raise ValueError('Label folder {} not a valid directory'.format(label_folder))
        self._image_folder_override = image_folder_override
        self._label_folder = label_folder
        # self._invalid_image_refs = ()
        self._dataframe = pd.DataFrame()
        self._ignore_missing_images = include_missing_images

    def fit(self, validate_images=False):
        """TODO: docstring"""
        if validate_images:
            warn("Validating images can be very slow on large datasets.")
            # TODO: add actual validation of images
        label_files = glob.glob(os.path.join(self._label_folder, '*.xml'))
        objects_df = pd.DataFrame()
        for label_file in label_files:
            with open(label_file, 'r') as file:
                xml = etree.fromstring(file.read())
                new_df = self.__xml_to_dataframe(xml)
                objects_df = pd.concat([objects_df, new_df])
        self._dataframe = objects_df
        return self

    def read(self):
        pass

    def __xml_to_dataframe(self, xml):
        """ TODO: docstring"""
        if self._image_folder_override is None:
            image_id = str(PurePath(xml.find('path').text))  # PurePath handles POSIX / Win32 differences
        else:
            image_id = str(PurePath(self._image_folder_override).joinpath(PurePath(xml.find('filename').text)))
        if not self._ignore_missing_images:
            if not os.path.isfile(image_id):  # check for invalid image file
                self._invalid_image_refs = self._invalid_image_refs + (image_id,)
                return pd.DataFrame()
        image_width = xml.find('size').find('width').text
        image_height = xml.find('size').find('height').text
        image_depth = xml.find('size').find('depth').text
        objects = []
        for item in xml:
            if item.tag == 'object':
                objects.append({'class_name': item.find('name').text,
                                'x_min': item.find('bndbox').find('xmin').text,
                                'x_max': item.find('bndbox').find('xmax').text,
                                'y_min': item.find('bndbox').find('ymin').text,
                                'y_max': item.find('bndbox').find('ymax').text
                                })
        objects = pd.DataFrame(objects)
        for item in ['image_id', 'image_width', 'image_height', 'image_depth']:
            objects[item] = eval(item)
        objects['retrieval_func'] = 'pascalvoc_image_reader'
        return objects


class PascalVOCWriter:

    def __init__(self):
        raise NotImplemented
