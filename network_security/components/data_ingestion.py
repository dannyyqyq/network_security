from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

import os
import sys
import pymongo
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split

# Configurations for data ingestion configuration
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact
from config.database_config import DatabaseConfig


database_config = DatabaseConfig("mongodb")
MONGO_DB_URI = database_config.MONGO_DB_URI


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Export the collection from the MongoDB database as a pandas dataframe
        Arg:
            None
        Returns:
            pd.DataFrame: The collection from the MongoDB database as a pandas dataframe
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.tolist():
                df = df.drop(columns=["_id"])

            df.replace({"na": np.nan}, inplace=True)

            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_to_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Export the data to the feature store
        Arg:
            dataframe(pd.DataFrame): The data to be exported to the feature store
        Returns:
            pd.DataFrame: The data that was exported to the feature store
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_path
            # Creation of folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data(self, dataframe: pd.DataFrame) -> List[pd.DataFrame]:
        try:
            train_test_split_ratio = self.data_ingestion_config.train_test_split_ratio
            train_set, test_set = train_test_split(
                dataframe, test_size=train_test_split_ratio, random_state=42
            )

            logging.info(
                f"Performed train test split on dataframe with split ratio :\
                         {train_test_split_ratio}"
            )
            logging.info(f"Train set shape: {train_set.shape}")
            logging.info(f"Test set shape: {test_set.shape}")
            logging.info(
                "Exited split data as train and test set of data ingestion class"
            )

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Created directory path: {dir_path}")
            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False)
            test_set.to_csv(self.data_ingestion_config.data_ingestion_path, index=False)
            logging.info("Completed exportion of train and test file path")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.data_ingestion_path,
            )

            logging.info(f"Data ingestion artifact : {data_ingestion_artifact}")

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
