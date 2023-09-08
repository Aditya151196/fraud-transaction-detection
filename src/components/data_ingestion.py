from src.entity.config_entity import DataIngestionConfig
import os,sys
from src.exception.exception import CustomException
from src.logger import *
from src.constants import *
from src.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
import tarfile
from six.moves import urllib
import shutil
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion log started.{'<<'*20}")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise CustomException(e,sys)
    
    def download_dataset(self) ->str:
        try:
            # url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir,exist_ok=True)

            banking_file_name = FILE_NAME

            raw_data_file_path = os.path.join(raw_data_dir,banking_file_name)

            logging.info(f"Downloading file from: [{download_url}] into :[{raw_data_file_path}]")
            urllib.request.urlretrieve(download_url,raw_data_file_path)
            logging.info(f"File :[{raw_data_file_path}] has been downloaded sucessfully.")
            return raw_data_file_path
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_downloaded_dataset(self)->str:
        try:
            # folder location to retrieve the file
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir,exist_ok=True)
            logging.info("Raw data directory...")

            banking_file_name = FILE_NAME
            raw_data_file_path = os.path.join(raw_data_dir,banking_file_name)

            # local location of dataset
            dataset_location = self.data_ingestion_config.dataset_local_location

            # copy the file from dataset location to raw data file
            shutil.copy(dataset_location,raw_data_file_path)
            logging.info(f"File copied from {dataset_location} to {raw_data_file_path}")

            return raw_data_file_path
        except Exception as e:
            raise CustomException(e,sys)
        
    def split_data_as_train_test(self,raw_data_file_path)->DataIngestionArtifact:
        try:
            banking_file_path = raw_data_file_path
            
            logging.info(f"Reading csv file: [{banking_file_path}]")
            banking_data_frame = pd.read_csv(banking_file_path)
            
            fraud_df = banking_data_frame.loc[banking_data_frame["isFraud"] == 1]
            non_fraud_df = banking_data_frame[banking_data_frame["isFraud"] == 0][:len(fraud_df)]
            banking_data_frame = pd.concat([fraud_df,non_fraud_df])

            # reset index
            banking_data_frame.reset_index(drop=True,inplace=True)

            banking_data_frame["cat_amount"] = pd.cut(
                banking_data_frame["amount"],
                4,
                labels = [1,2,3,4]
            )

            logging.info(f"Splitting data into train and test")
            #to keep the distribution equivalent in train and test dataset we make a new category on which we split using strat. shuffle split
            strat_train_set = None
            strat_test_set = None

            sss = StratifiedShuffleSplit(n_splits=1,test_size=0.2, random_state=42)

            for train_index,test_index in sss.split(banking_data_frame,banking_data_frame["cat_amount"]):
                strat_train_set = banking_data_frame.loc[train_index].drop(["cat_amount"], axis=1)
                strat_test_set = banking_data_frame.loc[test_index].drop(["cat_amount"], axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,FILE_NAME)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,FILE_NAME)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting train dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data Ingestion completed successfully")
            
            logging.info(f"Data Ingestion artifact: [{data_ingestion_artifact}]")
            return data_ingestion_artifact
        
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            raw_data_file_path = self.get_downloaded_dataset()
            return self.split_data_as_train_test(raw_data_file_path)
        except Exception as e:
            raise CustomException(e,sys)