from network_security.entity.artifact_entity import DataValidationArtifact
from network_security.entity.artifact_entity import DataIngestionArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import read_yaml_file
from network_security.utils.main_utils.utils import write_yaml_file
from network_security.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame):
        try:
            num_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns: {num_of_columns}")
            logging.info(f"Number of columns in data: {len(dataframe.columns)}")
            if len(dataframe.columns) == num_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_data_drift(self, base_df, current_df, threshold=0.05) -> None:
        try:
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_distribution = ks_2samp(d1, d2)
                if threshold < is_same_distribution.pvalue:
                    is_found = False
                else:
                    is_found = True
                report.update(
                    {
                        column: {
                            "p_value": float(is_same_distribution.pvalue),
                            "drift_status": is_found,
                        }
                    }
                )
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(
                file_path=drift_report_file_path,
                content=report,
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self):
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # read data from train and test path
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            # validate number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = "Trained dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = (
                    f"{error_message} Test dataframe does not contain all columns.\n"
                )

            # check for datadrift
            status = self.detect_data_drift(
                base_df=train_dataframe, current_df=test_dataframe
            )
            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=True,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info(f"Data validation artifact : {data_validation_artifact}")

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
