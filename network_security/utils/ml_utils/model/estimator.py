from network_security.exception.exception import NetworkSecurityException
import sys


class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, data):
        try:
            preprocessed_data = self.preprocessor.transform(data)
            y_pred = self.model.predict(preprocessed_data)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e, sys)
