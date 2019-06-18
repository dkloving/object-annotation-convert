import pandas as pd
from warnings import warn


class Dataset(object):

    required_columns = ['image_id', 'image_width', 'image_height', 'image_depth', 'x_min',
                        'x_max', 'y_min', 'y_max', 'class_id', 'class_name']

    def __init__(self, source_object=None, image_read_method=None, **kwargs):
        self.__subdatasets = [self]
        if image_read_method is None:
            self.image_read_method = lambda x: x
            warn("No image_read_method provided. Without a valid method or function, it will not be possible\
                 to read binary image data. This may be set after construction, but it is not recommended.")
        else:
            self.image_read_method = image_read_method

        if source_object is None:
            self.__dataframe = pd.DataFrame(data=None, columns=Dataset.required_columns)

        else:
            if type(source_object) == list:  # for combining multiple Datasets
                if all([type(obj) == Dataset for obj in source_object]):
                    self.__dataframe = None
                    self.__subdatasets = [subset for dataset in source_object for subset in dataset.__subdatasets]
                else:
                    self.__dataframe = pd.DataFrame(source_object)
            else:
                if type(source_object) == pd.DataFrame:  # for creating directly from pandas
                    self.__dataframe = source_object
                else:
                    self.__dataframe = pd.DataFrame(source_object)

        # final check of required columns
        for dataset in self.__subdatasets:
            if not all([c in dataset.__dataframe for c in Dataset.required_columns]):
                raise AttributeError('Must include columns for all of {}'.format(Dataset.required_columns))

    def read(self, idx):
        if not idx < len(self):
            raise IndexError("Requested index {} out of bounds for Dataset with length {}.".format(idx, len(self)))
        for subset in self.__subdatasets:
            if idx >= len(subset):
                idx = idx - len(subset)
            else:
                row = subset.__dataframe.iloc[idx].to_dict()
                image = subset.image_read_method(row['image_id'])
                return row, image

    def __len__(self):
        return sum([len(subset.__dataframe) for subset in self.__subdatasets])

    def __add__(self, other):
        assert type(other) == Dataset, 'Addition only defined when both objects are Datasets.'
        return Dataset([self, other])

    def __iter__(self):
        return self.__generate_rows()

    def __generate_rows(self):
        for i in range(len(self)):
            yield self.read(i)
