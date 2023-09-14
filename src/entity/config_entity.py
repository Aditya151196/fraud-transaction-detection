from collections import namedtuple

# Defining the inputs of different components

DataIngestionConfig = namedtuple("DataIngestionConfig",
                                 ["dataset_download_url","raw_data_dir","ingested_train_dir",
                                  "ingested_test_dir","dataset_local_location"])
"""Brings data into the system"""

DataValidationConfig = namedtuple("DataValidationConfig",
                                  ["schema_file_path","report_file_path","report_page_file_path"])

"""Schema validation - validating number of columns,types of columns,
detecting data drift,model drift if any
"""

DataTransformationConfig = namedtuple("DataTransformationConfig",
                                      ["transformed_train_dir",
                                       "transformed_test_dir",
                                       "preprocessed_object_file_path"])

"""EDA and feature engineering """

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["artifact_dir"])