import sys
import certifi
import pymongo
import pandas as pd
from config.database_config import DatabaseConfig
from network_security.exception.exception import NetworkSecurityException
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.utils.ml_utils.model.estimator import NetworkModel

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from network_security.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)
from network_security.utils.main_utils.utils import load_object

database_config = DatabaseConfig("mongodb")
MONGO_DB_URI = database_config.MONGO_DB_URI

print(MONGO_DB_URI)
ca = certifi.where()
mongo_client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
database = mongo_client[DATA_INGESTION_DATABASE_NAME]
collection = mongo_client[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

# Add middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response(
            content="Training pipeline started successfully", status_code=200
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        # Load preprocessor and model with error checking
        preprocessor = load_object("final_model/preprocessor.pkl")
        if preprocessor is None:
            raise NetworkSecurityException("Failed to load preprocessor")
        model = load_object("final_model/model.pkl")
        if model is None:
            raise ValueError("Failed to load model")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        y_pred = network_model.predict(df)
        print(y_pred)
        df["predicted_column"] = y_pred
        print(df["predicted_column"])
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes="table table-striped")
        # print(table_html)
        return templates.TemplateResponse(
            "table.html", {"request": request, "table": table_html}
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8080)
