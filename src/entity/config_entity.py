from collections import namedtuple

# Defining the inputs of different components

DataIngestionConfig = namedtuple("DataIngestionConfig",
                                 ["dataset_download_url","dataset_local_location","raw_data_dir","ingested_data_dir",
                                  "ingested_train_dir","ingested_test_dir"])
"""Brings data into the system"""

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["artifact_dir"])