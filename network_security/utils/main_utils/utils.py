from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import yaml
import os
import sys
import numpy as np
import pickle


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
