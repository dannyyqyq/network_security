from network_security.exception.exception import NetworkSecurityException
import yaml


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException("Failed to read yaml file", e)
