### Import Libraries
import os
import re
import numpy as np 
import pandas as pd
import dask
import dask.dataframe as dd
from dask.delayed import delayed
from ast import literal_eval
import sys
import config as cfg
from datetime import datetime

# Parameters
_DATSET_DIR = cfg.dirs["data_dir"]
_RAW_FILE_NAME = cfg._RAW_FILE_NAME
_RAW_SHEET_NAME = cfg._RAW_SHEET_NAME
_RAW_DATA_TYPE = cfg._RAW_DATA_TYPE
_PROCESSED_DATA_TYPE = cfg._PROCESSED_DATA_TYPE
_PROCESSED_FILE_NAME = cfg._PROCESSED_FILE_NAME
_PARQUETED_FILE_NAME = cfg._PARQUETED_FILE_NAME

class Dataset():

    def __init__(self, filename):
        
        # load dataset and convert into a parquet file ....
        if os.path.exists(os.path.join(_DATSET_DIR, "processed", _PARQUETED_FILE_NAME)):
            print("File has been already converted to parqueted format...")
            # Load data from parquet
            self._ds = dd.read_parquet( \
                os.path.join(_DATSET_DIR, "processed", _PARQUETED_FILE_NAME), \
                columns=_RAW_DATA_TYPE.keys(), \
                engine='pyarrow')

        else:
            # Parallelize code with dask.delayed
            self._ds = dask.delayed(pd.read_excel)( \
                            os.path.join(_DATSET_DIR, "raw", filename), \
                            sheet_name=_RAW_SHEET_NAME )
            # Convert into dask dataframe
            self._ds = dd.from_delayed( self._ds )
            # Save the file
            filename = os.path.join(
                                _DATSET_DIR, 
                                "processed", 
                                _PARQUETED_FILE_NAME)
            self.save_as_parquet(filename)
        

    def __len__(self):
        return len(self._ds)

    def __getitem__(self, index):
        'Retrun dataset as dataframe'
        X = self._ds.loc[index, :]    
        return X

    def save_as_parquet(self, filename) -> None:
        self._ds.to_parquet(filename, engine='pyarrow')

    def process_dataset(self):
        
        # Split the column "Interface Payment Ref" 
        # into "TAP IN TIME", "TAP IN ID", "TAP OUT TIME", "TAP OUT ID" 
        def remove_delimiters(x):
            return literal_eval(x) # Convert array like string into array

        def timestring_to_datetime(x, timestring_format= '%Y%m%dT%H%M%S'):
            return datetime.strptime(x, timestring_format)

        self._ds['Transaction Day'] = self._ds["Transaction Date"].apply(lambda x: timestring_to_datetime(x, timestring_format= '%Y-%m-%d %H:%M:%S'), meta=(datetime))
        self._ds['Transaction Hour'] = self._ds["Transaction Day"].apply(lambda x: x.hour, meta=(datetime))
        self._ds['Transaction Day'] = self._ds["Transaction Day"].apply(lambda x: x.dayofweek, meta=(datetime))

        self._ds['TAP IN TIME'] = self._ds["Interface Payment Ref"].apply(lambda x: remove_delimiters(x)[0], meta=(list))
        self._ds['TAP IN ID'] = self._ds["Interface Payment Ref"].apply(lambda x: remove_delimiters(x)[1], meta=(list))
        self._ds['TAP OUT TIME'] = self._ds["Interface Payment Ref"].apply(lambda x: remove_delimiters(x)[2], meta=(list))
        self._ds['TAP OUT ID'] = self._ds["Interface Payment Ref"].apply(lambda x: remove_delimiters(x)[3], meta=(list))
        
        # Convert time strings into datetime object
        self._ds['TAP IN TIME'] = self._ds["TAP IN TIME"].apply(lambda x: timestring_to_datetime(x), meta=(datetime))
        self._ds['TAP OUT TIME'] = self._ds["TAP OUT TIME"].apply(lambda x: timestring_to_datetime(x), meta=(datetime))
        
        # Split the datetime columns into Time and Date
        self._ds['TAP IN DATE'] = self._ds["TAP IN TIME"].apply(lambda x: str(x).split(" ")[0], meta=(str))
        self._ds['TAP OUT DATE'] = self._ds["TAP OUT TIME"].apply(lambda x: str(x).split(" ")[0], meta=(str))
        
        self._ds['TAP IN TIME'] = self._ds["TAP IN TIME"].apply(lambda x: str(x).split(" ")[1], meta=(str))
        self._ds['TAP OUT TIME'] = self._ds["TAP OUT TIME"].apply(lambda x: str(x).split(" ")[1], meta=(str))
        

        filename = os.path.join(
                            _DATSET_DIR, 
                            "processed", 
                            _PROCESSED_FILE_NAME)
        self.save_as_parquet(filename)



class DatasetLoader():
    def __init__(self, filename):
        'Load Dataset'
        c1 = Dataset(filename)
        print(c1._ds.head())
        print("C1 >>>>>>>>>>>>>>>>>")
        print(type(c1._ds))
        print(len(c1))
        c1.process_dataset()
        print(c1._ds.head())
        

if __name__ == "__main__":
    c2 = DatasetLoader(_RAW_FILE_NAME)
    