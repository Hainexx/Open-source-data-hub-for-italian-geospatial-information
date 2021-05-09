from abc import ABC, abstractmethod
import os


class BaseDataSource(ABC):

    def __init__(self, data_source_name):
        self.data_source_name = data_source_name
        if not os.path.isdir('raw_data'):
            os.mkdir('raw_data')
        self.data_source_path = os.path.join('raw_data', self.data_source_name)
        self.data = None

    @abstractmethod
    def download_data(self):
        pass

    def get_data(self):
        return self.data

    def save_data_to_csv(self, csv_filename):
        if not os.path.isdir(self.data_source_path):
            os.mkdir(self.data_source_path)

        filepath = os.path.join(self.data_source_path, f'{csv_filename}.csv')
        self.data.to_csv(filepath, index=False)
