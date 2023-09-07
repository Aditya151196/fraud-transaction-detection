import yaml
from src.exception.exception import CustomException
import os,sys
import numpy as np
import pandas as pd
import dill
from src.constants import *

def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as dictionary
    """

    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise CustomException(e,sys)