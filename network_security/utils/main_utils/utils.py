from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import yaml
import os
import sys
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns the contents as a dictionary.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.
    """
    try:
        with open(file_path, "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException("Failed to read yaml file", e)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes a YAML file with the given content.

    Args:
        file_path (str): The path to the YAML file.
        content (object): The content to be written to the YAML file.
        replace (bool, optional): Whether to replace the file if it exists. Defaults to False.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path: str, array: np.ndarray):
    """
    Saves a numpy array to a file.

    Args:
        file_path (str): The path to the file.
        array (np.ndarray): The numpy array to be saved.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_numpy_array_data(file_path: str):
    """
    Loads a numpy array from a file.

    Args:
        file_path (str): The path to the file.
        array (np.ndarray): The numpy array to be loaded.

    Returns:
        np.ndarray: The loaded numpy array.
    """
    try:
        with open(file_path, "rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_object(file_path: str, obj: object):
    """
    Saves an object to a file using pickle.

    Args:
        file_path (str): The path to the file.
        obj (object): The object to be saved.
    """
    try:
        logging.info("Entered the save_object method of main_utils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info("Saved the object successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def load_object(file_path: str):
    """
    Loads an object from a file using pickle.

    Args:
        file_path (str): The path to the file.
        obj (object): The object to be loaded.
    """

    try:
        if not os.path.exists(file_path):
            raise Exception(f"File not found at {file_path}")
        with open(file_path, "rb") as file_object:
            print(file_object)
            pickle.load(file_object)
        logging.info("Saved the object successfully")
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        report = {}

        # Iterate over models and their corresponding parameters
        for model_name, model in models.items():
            para = param.get(model_name, {})

            # Use GridSearchCV to find the best hyperparameters
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            # Set the best parameters and fit the model
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            # Get predictions but we are only using the best test score to select model
            # y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Calculate R2 score for train and test but we are only using the best test score to select model
            # train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            # Add the result to the report
            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
