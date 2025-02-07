from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.utils.ml_utils.model.estimator import NetworkModel
import os
import sys
from network_security.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from network_security.utils.ml_utils.metric.classification_metric import (
    get_classification_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
)
import mlflow
import dagshub

dagshub.init(repo_owner="dannyyqyq", repo_name="network_security", mlflow=True)


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision
            recall_score = classification_metric.recall

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(best_model, "model")

    def train_model(self, X_train, y_train, X_test, y_test):
        try:
            models = {
                "Logistic Regression": LogisticRegression(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(verbose=1),
                "Gradient Boost": GradientBoostingClassifier(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
                "K-Neighbors": KNeighborsClassifier(),
            }

            params = {
                "Decision Tree": {
                    "criterion": ["gini", "entropy", "log_loss"],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest": {
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    # 'max_features':['sqrt','log2',None],
                    "n_estimators": [8, 16, 32, 128, 256]
                },
                "Gradient Boosting": {
                    # 'loss':['log_loss', 'exponential'],
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "subsample": [0.6, 0.7, 0.75, 0.85, 0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Logistic Regression": {},
                "AdaBoost": {
                    "learning_rate": [0.1, 0.01, 0.001],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
            }

            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            best_model_name = None
            best_model_score = -float("inf")  # Start with a very low score

            # Iterate through the model report to find the best model
            for model_name, score in model_report.items():
                if score > best_model_score:
                    best_model_name = model_name
                    best_model_score = score

            # Retrieve the best model
            best_model = models[best_model_name]

            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_score(
                y_true=y_train, y_pred=y_train_pred
            )
            # Track MLflow
            self.track_mlflow(best_model, classification_train_metric)
            logging.info(f"train accuracy: {classification_train_metric}")

            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(
                y_true=y_test, y_pred=y_test_pred
            )
            # Track MLflow
            self.track_mlflow(best_model, classification_test_metric)
            logging.info(f"test accuracy: {classification_test_metric}")

            preprocessor = load_object(
                file_path=self.data_transformation_artifact.transformed_object_file_path
            )
            model_dir_path = os.path.dirname(
                self.model_trainer_config.trained_model_file_path
            )
            os.makedirs(model_dir_path)

            Network_Model = NetworkModel(preprocessor, best_model)
            logging.info(f"Network_Model : {Network_Model}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=Network_Model,
            )

            save_object("final model/model.pkl", best_model)

            # Model trainer artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_file_path=classification_train_metric,
                test_metric_file_path=classification_test_metric,
            )

            logging.info(f"Model trainer artifact : {model_trainer_artifact}")

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            # loading of training and testing arrays
            train_array = load_numpy_array_data(train_file_path)
            test_arrray = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_arrray[:, :-1],
                test_arrray[:, -1],
            )

            model = self.train_model(X_train, y_train, X_test, y_test)
            return model
        except Exception as e:
            raise NetworkSecurityException(sys, e)
