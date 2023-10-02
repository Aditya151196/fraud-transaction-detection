from collections import namedtuple

# Defining the outputs of different components
DataIngestionArtifact = namedtuple("DataIngestionArtifact",
                                   ["train_file_path","test_file_path","is_ingested","message"])

DataValidationArtifact = namedtuple("DataValidationArtifact",
                                    ["schema_file_path","report_file_path","report_page_file_path"
                                     ,"is_validated","message"])

DataTransformationArtifact = namedtuple("DataTransformationArtifact",
                                        ["is_transformed","message","transformed_train_file_path",
                                         "transformed_test_file_path","preprocessed_object_file_path"])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact",
                                  ["is_trained","message","trained_model_path","train_prec",
                                   "test_prec","train_accuracy","test_accuracy","model_accuracy"])