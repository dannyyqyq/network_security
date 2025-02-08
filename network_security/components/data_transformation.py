from network_security.exception.exception import NetworkSecurityException
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from network_security.constants.training_pipeline import TARGET_COLUMN
from network_security.constants.training_pipeline import (
    DATA_TRANSFORMATION_IMPUTED_PARAMS,
)
from network_security.entity.artifact_entity import (
    DataValidationArtifact,
    DataTransformationArtifact,
)
from network_security.entity.config_entity import DataTransformationConfig
from network_security.logging.logger import logging
from network_security.utils.main_utils.utils import save_object, save_numpy_array_data


class DataTransformation:
    def __init__(
        self,
        datavalidation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.datavalidation_artifact: DataValidationArtifact = (
                datavalidation_artifact
            )
            self.data_transformation_config: DataTransformationConfig = (
                data_transformation_config
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def get_data_transformation_pipeline_object(self) -> Pipeline:
        """
        Creates and returns a data transformation pipeline object.

        This pipeline includes a KNNImputer for handling missing values in the dataset.
        The imputer is initialized with parameters specified in DATA_TRANSFORMATION_IMPUTED_PARAMS.

        Returns:
            Pipeline: A scikit-learn Pipeline object that includes a KNNImputer step.

        """
        try:
            logging.info("Creating data transformation pipeline")
            knn_imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTED_PARAMS)
            logging.info(
                f"Initialized KNNImputer with parameters: {DATA_TRANSFORMATION_IMPUTED_PARAMS}"
            )
            processor: Pipeline = Pipeline([("knn_imputer", knn_imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiating Data Transformation method of transformation class")
        try:
            logging.info("Starting data transformation")
            train_df = self.read_data(
                self.datavalidation_artifact.valid_train_file_path
            )
            test_df = self.read_data(self.datavalidation_artifact.valid_test_file_path)

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            preprocessor = self.get_data_transformation_pipeline_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(
                input_feature_train_df
            )
            transformed_input_test_feature = preprocessor_object.transform(
                input_feature_test_df
            )

            # combined back both arrays using numpy.c
            train_array = np.c_[
                transformed_input_train_feature, np.array(target_feature_train_df)
            ]
            test_array = np.c_[
                transformed_input_test_feature, np.array(target_feature_test_df)
            ]

            # save the numpy arrays
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path, train_array
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path, test_array
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )

            save_object("final_model/preprocessor.pkl", preprocessor_object)

            # prepare artifacts
            data_trasformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info(
                f"Data transformation artifact : {data_trasformation_artifact}"
            )

            return data_trasformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
