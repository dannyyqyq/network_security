import sys
import json
import certifi
import pandas as pd
import pymongo
from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from config.database_config import DatabaseConfig


class NetWorkDataExtract:
    def cv_to_json_converter(self, filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True, inplace=True)
            data_json = json.loads(data.to_json(orient="records", lines=False))
            # data_json = list(json.loads(data.T.to_json()).values())
            return data_json
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(
        self, MONGO_DB_URI, data_json, database_name, collection_name
    ):
        try:
            self.database_name = database_name
            self.collection_name = collection_name
            self.data_json = data_json

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            self.database_name = self.mongo_client[self.database_name]
            self.collection_name = self.database_name[self.collection_name]

            self.collection_name.insert_many(self.data_json)
            return len(self.data_json)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    # The certifi.where() call is used for SSL certificate verification when making secure connections:
    ca = certifi.where()

    database_config = DatabaseConfig("mongodb")

    network_object = NetWorkDataExtract()
    data_json = network_object.cv_to_json_converter(database_config.FILE_PATH)
    num_of_records = network_object.insert_data_to_mongodb(
        database_config.MONGO_DB_URI,
        data_json,
        database_config.DATABASE_NAME,
        database_config.COLLECTION_NAME,
    )
    logging.info(f"Number of records inserted to MongoDB: {num_of_records}")
    logging.info("Successfully pushed data to MongoDB")
