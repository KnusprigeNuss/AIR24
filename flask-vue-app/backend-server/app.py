import os
import sys
from time import sleep

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from ai_models.HealthPredictorAndRecommender import \
    HealthPredictorAndRecommender

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

predictor = HealthPredictorAndRecommender()

@app.route('/submit', methods=['POST'])
def handle_submit():
    response = {}

    sleep(0.4)

    try:
        person_data = request.get_json()
        response['person_data'] = person_data

        # Predict heart disease based on the input data
        prediction = predictor.predict_heart_disease(person_data)

        response['HeartDisease'] = prediction

        if prediction == 'Yes':
            response['DrugRecommendations'] = predictor.get_drug_recommendation(person_data)
        else:
            response['DrugRecommendations'] = None

    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        response['error'] = str(e)

    return jsonify(response)

if __name__ == '__main__':
    app.run()
