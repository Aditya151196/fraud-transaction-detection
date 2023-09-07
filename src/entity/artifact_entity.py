from collections import namedtuple

# Defining the outputs of different components
DataIngestionArtifact = namedtuple("DataIngestionArtifact",
                                   ["train_file_path","test_file_path","is_ingested","message"])
