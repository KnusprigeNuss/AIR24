import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
  # Basic DataBase
  drugs_db_ = pd.read_csv('../../data/drug-dataset/Medicine_Details.csv')

  # Synonyms - Definitions
  medication_types_to_exclude_ = ['Drop'] # Exclude eye drops

  heart_string_           = ['heart', 'cardiovascular', 'pressure'] # Get different types of heart synonyms to filter out only those first.
  
  alcohol_string_         = ['alcohol', 'drinking', 'alcoholic', 'liver']
  asthma_string_          = ['asthma', 'breathing', 'inhaler', 'wheezing', 'cough', 'respiratory', 'lung']
  bmi_string_             = ['bmi', 'body', 'mass', 'index', 'weight', 'obesity']
  diabetes_string_        = ['diabetes', 'sugar', 'insulin', 'glucose']
  kidney_disease_string_  = ['kidney', 'disease', 'renal', 'failure', 'dialysis', 'urine']
  mental_health_string_   = ['mental', 'health', 'depression', 'anxiety', 'stress', 'psychological']
  physical_health_string_ = ['physical', 'health', 'exercise', 'workout', 'gym', 'fitness', 'fit']
  skin_cancer_string_     = ['skin', 'cancer', 'melanoma', 'mole', 'sun', 'uv']
  sleep_time_string_      = ['sleep', 'time', 'tired', 'fatigue', 'rest', 'nap']
  smoking_string_         = ['smoking', 'cigarette', 'nicotine', 'tobacco', 'respiratory', 'lung', 'throat']
  stroke_string_          = ['stroke', 'brain', 'paralysis', 'hemorrhage', 'clot', 'Dizziness', 'Headache', 'Nausea']
  
  

  def __init__(self, user_data: dict):
    user_df = pd.DataFrame([user_data])
    self.user_data_ = user_df.drop(columns=['HeartDisease', 'DiffWalking', 'AgeCategory', 'GenHealth', 'PhysicalActivity', 'Race', 'Sex']).to_dict(orient='records')[0]
    print(self.user_data_.items())
    self.alcohol_: bool = True if user_data['AlcoholDrinking'] == 'Yes' else False
    self.asthma_: bool = True if user_data['Asthma'] == 'Yes' else False
    self.bmi_: int = int(user_data['BMI'])
    self.diabetic_: bool = False if user_data['Diabetic'] == 'No' else True
    self.kidney_disease_: bool = True if user_data['KidneyDisease'] == 'Yes' else False
    self.mental_health_: int = int(user_data['MentalHealth'])
    self.physical_health_: int = int(user_data['PhysicalHealth'])
    self.skin_cancer_: bool = True if user_data['SkinCancer'] == 'Yes' else False
    self.sleep_time_: int = int(user_data['SleepTime'])
    self.smoking_: bool = True if user_data['Smoking'] == 'Yes' else False
    self.stroke_: bool = True if user_data['Stroke'] == 'Yes' else False
  
  def getStringToFilter(self):
    conditions: list[str] = []
    if self.alcohol_:
      conditions.append('|'.join(self.alcohol_string_))
    if self.asthma_:
      conditions.append('|'.join(self.asthma_string_))
    if self.bmi_ > 25:  # Considered obese
      conditions.append('|'.join(self.bmi_string_))
    if self.diabetic_:
      conditions.append('|'.join(self.diabetes_string_))
    if self.kidney_disease_:
      conditions.append('|'.join(self.kidney_disease_string_))
    if self.mental_health_ <= 5:
      conditions.append('|'.join(self.mental_health_string_))
    if self.physical_health_ <= 5:
      conditions.append('|'.join(self.physical_health_string_))
    if self.skin_cancer_:
      conditions.append('|'.join(self.skin_cancer_string_))
    if self.sleep_time_ <= 5 or self.sleep_time_ >= 11:
      conditions.append('|'.join(self.sleep_time_string_))
    if self.smoking_:
      conditions.append('|'.join(self.smoking_string_))
    if self.stroke_:
      conditions.append('|'.join(self.stroke_string_))
    return conditions
  
  def getDrugRecommendation(self):
    conditions: list[str] = self.getStringToFilter()
    self.filtered_drug_db_ = self.drugs_db_[~self.drugs_db_['Medicine Name'].str.contains('|'.join(self.medication_types_to_exclude_), case=False, na=False)] # Filter out eye drops, since they are not relevant.
    
    # Get only medications against heart diseases    
    self.filtered_drug_db_ = self.filtered_drug_db_[self.filtered_drug_db_['Uses'].str.contains('|'.join(self.heart_string_), case=False, na=False)]
    
    combined_conditions: str = '|'.join(conditions + self.heart_string_)
    self.filtered_drug_db_ = self.filtered_drug_db_[~self.filtered_drug_db_['Side_effects'].str.contains(combined_conditions, case=False, na=False)]
    
    if conditions:
      self.filtered_drug_db_['priority'] = self.filtered_drug_db_['Uses'].str.contains('|'.join(conditions), case=False, na=False).astype(int)
      self.filtered_drug_db_ = self.filtered_drug_db_.sort_values(by='priority', ascending=False).drop(columns=['priority'])
  
  def getVectorizer(self):
    self.getDrugRecommendation()
    vectorizer: TfidfVectorizer = TfidfVectorizer()
    self.drug_vectors_ = vectorizer.fit_transform(self.filtered_drug_db_['Uses'])
    user_conditions = ' '.join([f'{k}:{v}' for k, v in self.user_data_.items()])
    self.user_vector_ = vectorizer.transform([user_conditions])
    
  def getSimilarityScores(self):
    self.similarity_scores_ = cosine_similarity(self.user_vector_, self.drug_vectors_).flatten()
    
  def getTopIndices(self):
    top_indices = self.similarity_scores_.argsort()[:5][::-1]
    return self.filtered_drug_db_.iloc[top_indices]
    
  

def test():
  user_input = {
    'AgeCategory': "80 or older",
    'AlcoholDrinking': 'Yes',
    'Asthma': 'Yes',
    'BMI': 35,
    'Diabetic': 'Yes',
    'DiffWalking': 'Yes',
    'GenHealth': 'Poor',
    'HeartDisease': 'Yes',
    'KidneyDisease': 'Yes',
    'MentalHealth': 29,
    'PhysicalActivity':'No',
    'PhysicalHealth': 29,
    'Race': 'White',
    'Sex': 'Male',
    'SkinCancer': 'Yes',
    'SleepTime': 2,
    'Smoking': 'Yes',
    'Stroke': 'Yes'    
  }
  recommender = Recommender(user_input)
  recommender.getVectorizer()
  recommender.getSimilarityScores()
  print(recommender.getTopIndices().to_dict(orient='records'))  
  
  
if __name__ == '__main__':
  test()
  