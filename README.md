# 🔒 Network Security System for Phishing Data End-to-End Deployment Project

## 📌 Project Overview

This project develops a system to detect phishing attempts by analyzing network data. It combines machine learning techniques with secure data storage and processing. This project covers:

- **Data Handling**: Efficient management of network data using MongoDB for secure storage and retrieval.
- **Data Ingestion**: Extracting data from various sources, converting it into a usable format, and preparing it for analysis.
- **Model Training**: Application of machine learning techniques like Random Forest, Decision Trees, and Gradient Boosting to train models for identifying phishing patterns.
- **Prediction Pipeline**: Utilizing trained models to make real-time predictions on new data.
- **Web Application**: Development of a FastAPI-based web application that serves as an interface for data input and prediction output.
- **Deployment**: Containerizing the application with Docker and employing CI/CD practices for seamless deployment across different environments, ensuring scalability and reliability.
  
## 🛠 Tools and Technologies

- **Python**: Core language for development.
- **MongoDB**: For data storage, particularly using MongoDB Atlas for cloud-based solutions.
- **Machine Learning**: Using Scikit-learn for model training, alongside MLflow for experiment tracking.
- **FastAPI**: For building a fast, modern, Python-based web API.
- **Docker**: For containerization and easy deployment.
- **CI/CD**: GitHub Actions for continuous integration and deployment.
- **Others**: `pymongo` for MongoDB interactions, `dill` for serialization, `pandas` for data manipulation, `certifi` for SSL certificate handling, AWS S3 for cloud storage.

### 🚀 Deployment & CI/CD
- **GitHub Actions**: Utilized for an automated CI/CD pipeline, ensuring code quality and consistency from development to production.
- **Docker**: Employed for containerization, which supports uniform deployment across different environments.
- **AWS S3**: Acts as storage for model artifacts, data backups, and logs, facilitating data preservation and recovery.
- **MongoDB Atlas**: Provides a scalable and secure database solution for data storage and management in the cloud.
  
## 📊 Key Features

- **Data Extraction and Storage**: Converts CSV to JSON, stores in MongoDB, and syncs with AWS S3.
- **Data Pipeline**: Comprehensive pipeline for data ingestion, validation, transformation, and model training.
- **Machine Learning**: Trains models with various classifiers to identify phishing patterns.
- **API**: Provides endpoints for real-time phishing detection:
  - **Training Pipeline**: Starts the training pipeline via an API call.
  - **Prediction**: Accepts CSV files for on-the-fly prediction and returns results in HTML.
- **Model and Data Sync**: Syncs local artifacts and models to S3 for cloud storage.
