import pandas as pd
from pathlib import Path
from warnings import warn

from modules.dataset import Dataset
from utils.io import read_image_file, write_image_file, validate_image


class CSVReader:
    """TODO: docstring"""

    def __init__(self, csv_file, image_folder_override=None):
        """TODO docstring"""
        if not Path(csv_file).is_file():
            raise ValueError('csv_file {} not a valid file'.format(csv_file))
        if image_folder_override is not None:
            if not Path(image_folder_override).is_dir():
                raise ValueError('Image folder {} not a valid directory'.format(image_folder_override))
        self._image_folder_override = image_folder_override
        self._csv_file = csv_file
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
        csv_df = pd.read_csv(self._csv_file)
        csv_df['image_valid'] = csv_df.apply(lambda row: validate_image(row['image_id'],
                                                                        deep_validate_images,
                                                                        row['image_width'],
                                                                        row['image_height'],
                                                                        row['image_depth']))
        self._dataframe = csv_df
        return self

    def _get_invalid_images(self):
        return self._dataframe[~self._dataframe.image_valid].image_id.unique()


class CSVWriter:

    def __init__(self, folder_root, ignore_not_empty=False, image_format='jpg'):
        self._folder_root = folder_root
        self._ignore_not_empty = ignore_not_empty
        self._image_format = image_format
        self.__prepare_folder()

    def __prepare_folder(self):
        path = Path(self._folder_root)
        if not path.exists():
            path.mkdir()
        else:  # Houston, we *may* have a problem...
            if not path.is_dir():  # ...our rocket ship is actually a rubber ducky, abort mission.
                assert ValueError("{} exists already but is not a directory.".format(self._folder_root))
            elif len([item for item in path.glob('*')]) > 0:  # ...There are Ruskies in our rocket ship...
                if not self._ignore_not_empty:  # ...abort mission
                    raise ValueError("{} is a valid directory but is not empty.\
                     folder_root must not exist or be empty unless ignore_not_empty is True.".format(path))
                else:  # ...they brought vodka for everyone, hope no one spacevomits.
                    warn("{} is not empty, but ignoring. This could cause problems.")

    def make_valid_filename(self, filename, k=0):
        k_str = '' if k == 0 else '_' + str(k)
        candidate_filename = Path(filename).stem + k_str + '.' + self._image_format
        if Path(candidate_filename).exists():
            return self.make_valid_filename(filename, k+1)

    def write_to_disk(self, dataset):
        df_to_write = pd.DataFrame(columns=Dataset.required_columns)
        for row, image in dataset:
            output_filename = self.make_valid_filename(row['image_id'])
            write_image_file(image, output_filename)
            row['image_id'] = output_filename
            df_to_write.append(row)
