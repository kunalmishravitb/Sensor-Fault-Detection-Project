from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from src.exception import CustomException
from src.logger import logging as lg
import os, sys

from src.pipeline.train_pipeline import TrainingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

app=Flask(__name__)

@cross_origin
@app.route("/")
def home():
    return "Welcome to my Application"


@cross_origin
@app.route("/train")
def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return "Training Completed."
    except Exception as e:
        raise CustomException(e, sys)


@cross_origin
@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        if request.method=='POST':
            # It is a object of prediction pipeline
            prediction_pipeline=PredictionPipeline(request)

            # Now we are running this run pipeline method
            prediction_file_detail=prediction_pipeline.run_pipeline()

            lg.info("Prediction Completed. Downloading Prediction File.")
            return send_file(prediction_file_detail.prediction_file_path,
                             download_name=prediction_file_detail.prediction_file_name,
                             as_attachment=True)
        else:
            return render_template('upload_file.html')
    except Exception as e:
        raise CustomException(e, sys)


# Execution will start from here
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
