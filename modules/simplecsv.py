import pandas as pd
import pathlib
from warnings import warn

from modules.dataset import Dataset
from utils.io import write_image_file


class SimpleCSVWriter:

    def __init__(self, folder_root, ignore_not_empty=False, image_format='jpg'):
        self._folder_root = folder_root
        self._ignore_not_empty = ignore_not_empty
        self._image_format = image_format
        self.__prepare_folder()

    def __prepare_folder(self):
        path = pathlib.Path(self._folder_root)
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
        candidate_filename = pathlib.Path(filename).stem + k_str + '.' + self._image_format
        if pathlib.Path(candidate_filename).exists():
            return self.make_valid_filename(filename, k+1)

    def write_to_disk(self, dataset):
        df_to_write = pd.DataFrame(columns=Dataset.required_columns)
        for row, image in dataset:
            output_filename = self.make_valid_filename(row['image_id'])
            write_image_file(image, output_filename)
            row['image_id'] = output_filename
            df_to_write.append(row)
