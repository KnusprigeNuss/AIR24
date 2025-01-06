import os
import pickle

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OrdinalEncoder

from ai_models.recommender_model.RecommenderModel import Recommender


class HealthPredictorAndRecommender:
    """
    This class provides functionalities for predicting the likelihood of heart disease based on user-provided information
    and generating personalized drug recommendations using pre-trained AI models.
    """

    def __init__(self):

        # Get the current working directory
        current_directory = os.getcwd()

        # Print the current working directory
        print("Current Working Directory:", current_directory)

        self.predict_disease_model_path = '../../ai_models/predict_disease_model/predict_disease_model.pkl'
        self.predict_disease_model = None
        self.predict_model_encoder_path = '../../ai_models/predict_disease_model/predict_model_encoder.pkl'
        self.predict_model_encoder = None

        self.recommender_model_path = '../../ai_models/recommender_model/recommender_model.pkl'
        self.vectorizer = None
        self.filtered_drugs_db = None
        self.drug_vectors = None

        # Load the models
        try:
            with open(self.predict_disease_model_path, 'rb') as file:
                self.predict_disease_model = pickle.load(file)
            print("Predict disease model loaded successfully.")
        except Exception as e:
            print(f"Failed to load disease prediction model. Reason: {e}")

        try:
            with open(self.predict_model_encoder_path, 'rb') as file:
                self.predict_model_encoder = pickle.load(file)
            print("Predict model encoder loaded successfully.")
        except Exception as e:
            print(f"Failed to load predict model encoder. Reason: {e}")

        try:
            with open(self.recommender_model_path, 'rb') as file:
                data = pickle.load(file)

            # Extract the objects
            self.vectorizer = data["vectorizer"]
            self.filtered_drugs_db = data["filtered_drugs_db"]
            self.drug_vectors = data["drug_vectors"]
            print("Recommender model loaded successfully.")
        except Exception as e:
            print(f"Failed to load recommender model. Reason: {e}")

    def predict_heart_disease(self, person_data):
        """
        Predict whether a person has heart disease based on their data.

        Parameters:
            person_data (dict): A dictionary containing the person's details (features), such as BMI,
                                smoking habits, age category, and general health.

        Returns:
            str: Prediction result - 'Yes' if the prediction indicates heart disease or 'No' otherwise.

        Raises:
            RuntimeError: If the heart disease prediction model has not been loaded successfully.
        """
        if not self.predict_disease_model:
            raise RuntimeError("Model is not loaded. Ensure the correct path is given during initialization.")
        if not self.predict_model_encoder:
            raise RuntimeError("Model encoder is not loaded. Ensure the correct path is given during initialization.")

        # Make single prediction

        # Convert the dictionary into a DataFrame
        person_dataframe = pd.DataFrame([person_data])

        object_cols = [
            "Smoking",
            "AlcoholDrinking",
            "Stroke",
            "DiffWalking",
            "Sex",
            "AgeCategory",
            "Race",
            "Diabetic",
            "PhysicalActivity",
            "GenHealth",
            "Asthma",
            "KidneyDisease",
            "SkinCancer"
        ]
        print(f'object_cols: {object_cols}')

        ordinal_person_dataframe = person_dataframe.copy()

        # Encode categorical data
        n = self.predict_model_encoder.transform(person_dataframe[object_cols])
        ordinal_person_dataframe[object_cols] = n
        print(f'n: {n}')

        # Reorder the dataframe to match the feature names to those that were passed during fit.
        # Feature names must be in the same order as they were in fit
        ordinal_person_dataframe = ordinal_person_dataframe[[
            "BMI",
            "Smoking",
            "AlcoholDrinking",
            "Stroke",
            "PhysicalHealth",
            "MentalHealth",
            "DiffWalking",
            "Sex",
            "AgeCategory",
            "Race",
            "Diabetic",
            "PhysicalActivity",
            "GenHealth",
            "SleepTime",
            "Asthma",
            "KidneyDisease",
            "SkinCancer"
        ]]

        print(f'opdf: {ordinal_person_dataframe}')

        # Utilizing model to predict HeartDisease based on person_data
        HeartDisease_prediction = self.predict_disease_model.predict(ordinal_person_dataframe)

        # Output the prediction
        print("Predicted Heart Disease Status:", HeartDisease_prediction[0])

        return 'Yes' if HeartDisease_prediction[0]==1 else 'No'

    def get_drug_recommendation(self, person_data):
        """
        Generate recommended drugs for a person based on their medical conditions and data.

        Parameters:
            person_data (dict): A dictionary containing a person's health conditions, symptoms,
                                and other relevant medical details.

        Returns:
            pd.DataFrame: A DataFrame containing the top 5 recommended drugs and related details.
        """

        # Example logic for matching user_data with drug_vectors to recommend drugs
        recommender = Recommender(person_data)
        recommender.getVectorizer()
        recommender.getSimilarityScores()
        return recommender.getTopIndices()
        # user_conditions = ' '.join([f'{k}:{v}' for k, v in person_data.items()])
        # user_vector = self.vectorizer.transform([user_conditions])

        # # Calculate the similarity between the user's vector and the drug vectors (cosine similarity)
        # similarity_scores = cosine_similarity(user_vector, self.drug_vectors).flatten()

        # top_indices = similarity_scores.argsort()[:5][::-1]
        # recommended_drugs = self.filtered_drugs_db.iloc[top_indices]

        # return recommended_drugs.to_dict(orient='records')
