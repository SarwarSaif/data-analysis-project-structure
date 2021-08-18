#!/usr/bin/env python
#import preprocessing
import os
_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')) # Move one directory up to get the base directory
_RAW_FILE_NAME = "SAMPLE_02-16_JUN_2019.xlsx" 
_RAW_SHEET_NAME = "RAW Data" 
_PARQUETED_FILE_NAME = "parqueted_mrt_transactions_data.parquet"
_PROCESSED_FILE_NAME = "processed_mrt_transactions_data.parquet" 
_RAW_DATA_TYPE = {
             'Transaction Date': 'object',
             'Emoney': 'str',
             'PAN': 'Int64',
             'amount': 'Int64',
             'Interface Payment Ref': 'str',
             'TAP IN': 'str',
             'TAP OUT': 'str',}

_PROCESSED_DATA_TYPE = {
             'Transaction Date': 'object',
             'Transaction Day': 'str',
             'Transaction Hour': 'str',
             'Emoney': 'str',
             'PAN': 'Int64',
             'amount': 'Int64',
             'TAP IN DATE': 'str',
             'TAP IN TIME': 'str',
             'TAP IN ID': 'str', 
             'TAP OUT DATE': 'str',
             'TAP OUT TIME': 'str',
             'TAP OUT ID': 'str',
             'TAP IN': 'str',
             'TAP OUT': 'str',}

dirs = {
    "base_dir": _BASE_DIR,
    "data_dir": os.path.join(_BASE_DIR,"input"),
    "out_dir": os.path.join(_BASE_DIR,"output"),
}

"""
preprocessing_queue = [
    preprocessing.scale_and_center,
    preprocessing.dot_reduction,
    preprocessing.connect_lines,
]
use_anonymous = True
"""
print(dirs)