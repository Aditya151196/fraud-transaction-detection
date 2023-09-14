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
    
def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file
    file_path:str
    data:dict
    """

    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_numpy_array_data(file_path:str,array:np.array):
    """
    save numpy array data to file
    file_path : str
    array : np.array
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CustomException(e,sys)
    
def load_numpy_array_data(file_path:str)->np.array:
    """ 
    load numpy array data from file
    file_path : str
    return :np.array format data
    """

    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_path)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path:str,obj):
    """
    file_path : str
    obj : Any sort of object
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(bj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path:str):
    """
    file_path : str
    """

    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    
def load_data(file_path: str, schema_file_path: str)->pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(schema_file_path)

        schema = dataset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe = pd.read_csv(file_path)

        error_message = ""

        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message} \n Column: [{column}] is not in the schema"
        if len(error_message)>0:
            raise Exception(error_message)
        return dataframe
    
    except Exception as e:
        raise CustomException(e,sys)