import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder

class HealthPredictorAndRecommender:
    def __init__(self, predict_disease_model_path):
        """
        Constructor to load the model from a given path.

        :param model_path: Path to the pre-trained model file (Pickle format).
        """
        self.model = None

        try:
            with open(predict_disease_model_path, 'rb') as file:
                self.model = pickle.load(file)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Failed to load model. Reason: {e}")

    def predict(self, person_data):
        """
        Predict whether a person has heart disease based on their data.

        :param person_data: A dictionary containing the person's details (features).
        :return: Prediction result (Yes/No) for Heart Disease.
        """
        if not self.model:
            raise RuntimeError("Model is not loaded. Ensure the correct path is given during initialization.")

        # Make single prediction

        # Convert the dictionary into a DataFrame
        person_dataframe = pd.DataFrame([person_data])

        s = (person_dataframe.dtypes == 'object')
        object_cols = list(s[s].index)

        ordinal_person_dataframe = person_dataframe.copy()

        # Encode categorical data
        ordinal_encoder = OrdinalEncoder()
        ordinal_person_dataframe[object_cols] = ordinal_encoder.fit_transform(person_dataframe[object_cols])

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

        # Utilizing model to predict HeartDisease based on person_data
        HeartDisease_prediction = self.model.predict(ordinal_person_dataframe)

        # Output the prediction
        print("Predicted Heart Disease Status:", HeartDisease_prediction[0])

        return 'Yes' if HeartDisease_prediction[0]==1 else 'No'
