import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

drugs_db = pd.read_csv('../../data/Medicine_Details.csv')

# Synonyms
medication_types_to_exclude = ['Drop'] # Exclude eye drops

heart = ['heart', 'cardiovascular', 'pressure']
alcohol = ['alcohol', 'drinking', 'alcoholic', 'liver']
smoking = ['smoking', 'cigarette', 'nicotine', 'tobacco']
stroke  = ['stroke', 'brain', 'paralysis', 'hemorrhage', 'clot', 'Dizziness', 'Headache', 'Nausea']
physical_health = ['physical', 'health', 'exercise', 'workout', 'gym', 'fitness', 'fit']
mental_health = ['mental', 'health', 'depression', 'anxiety', 'stress', 'psychological']
diff_walking = ['difficulty', 'walking', 'walk', 'move', 'mobility', 'paralysis']
diabetes = ['diabetes', 'sugar', 'insulin', 'glucose']
bmi = ['bmi', 'body', 'mass', 'index', 'weight', 'obesity']
generic_health = ['generic', 'health', 'overall', 'well-being', 'general']
sleep_time = ['sleep', 'time', 'tired', 'fatigue', 'rest', 'nap']
asthma = ['asthma', 'breathing', 'inhaler', 'wheezing', 'cough']
kidney_disease = ['kidney', 'disease', 'renal', 'failure', 'dialysis', 'urine']
skin_cancer = ['skin', 'cancer', 'melanoma', 'mole', 'sun', 'uv']
cholesterol = ['cholesterol', 'hdl', 'ldl', 'triglycerides', 'fat']

# Test user
user_input = {
    'HeartDisease': 'No',
    'BMI': 23,
    'Smoking': 'No',
    'Alcohol': 'No',
    'Stroke': 'No',
    'PhysicalHealth': 10,
    'MentalHealth': 10,
    'DiffWalking': 1,
    'Sex': 'Male',
    'Age': 21,
    'Diabetes': 'No',
    'PhysicalActivity': 10,
    'GenericHealth': 10,
    'SleepTime': 8,
    'Asthma': 'No',
    'KidneyDisease': 'No',
    'SkinCancer': 'No',
    # 'Cholesterol': 200,
    # 'BloodPressure': 120,
    'Allergies': ['penicillin', 'aspirin', 'Diarrhea', 'Bupropion']  
}

# User to df
user_df: pd.DataFrame = pd.DataFrame([user_input])

# Filter conditions for dataset
conditions = []
if user_input['Smoking'] == 'Yes':
    conditions.append('|'.join(smoking))
if user_input['Stroke'] == 'Yes':
    conditions.append('|'.join(stroke))
if user_input['Alcohol'] == 'Yes':
    conditions.append('|'.join(alcohol))
if user_input['Diabetes'] == 'Yes':
    conditions.append('|'.join(diabetes))
if user_input['Asthma'] == 'Yes':
    conditions.append('|'.join(asthma))
if user_input['KidneyDisease'] == 'Yes':
    conditions.append('|'.join(kidney_disease))
if user_input['SkinCancer'] == 'Yes':
    conditions.append('|'.join(skin_cancer))
# if user_input['Cholesterol'] > 200:
#     conditions.append('|'.join(cholesterol))
if user_input['BMI'] > 25:
    conditions.append('|'.join(bmi))
if user_input['PhysicalHealth'] < 3:
    conditions.append('|'.join(physical_health))
if user_input['MentalHealth'] < 3:
    conditions.append('|'.join(mental_health))
if user_input['GenericHealth'] < 3:
    conditions.append('|'.join(generic_health))
if user_input['SleepTime'] < 7:
    conditions.append('|'.join(sleep_time))
if user_input['DiffWalking'] > 3:
    conditions.append('|'.join(diff_walking))

# Filter dataset
filtered_drugs_db = drugs_db[~drugs_db['Medicine Name'].str.contains('|'.join(medication_types_to_exclude), case=False, na=False)]

filtered_drugs_db = filtered_drugs_db[filtered_drugs_db['Uses'].str.contains('|'.join(heart), case=False, na=False)]

# Further filter based on conditions and heart-related side effects
if conditions:
    combined_conditions = '|'.join(conditions + heart)
    filtered_drugs_db = filtered_drugs_db[~filtered_drugs_db['Side_effects'].str.contains(combined_conditions, case=False, na=False)]

# Prioritize entries that match the conditions in the Uses column
# if conditions:
#     filtered_drugs_db['priority'] = filtered_drugs_db['Uses'].str.contains('|'.join(conditions), case=False, na=False).astype(int)
#     filtered_drugs_db = filtered_drugs_db.sort_values(by='priority', ascending=False).drop(columns=['priority'])

# filtered_drugs_db = drugs_db[drugs_db['Uses'].str.contains('|'.join(heart), case=False, na=False)]
# filtered_drugs_db = drugs_db[drugs_db['Uses'].str.contains('|'.join(conditions), case=False, na=False)]
# filtered_drugs_db = filtered_drugs_db[~filtered_drugs_db['Side_effects'].str.contains('|'.join(conditions).join(heart), case=False, na=False)]
print("Filtered Drugs:")
print(filtered_drugs_db)

# Exclude words from Composition column
allergies = user_input['Allergies']
if allergies:
    allergy_pattern = '|'.join(allergies)
    filtered_drugs_db = filtered_drugs_db[~filtered_drugs_db['Composition'].str.contains(allergy_pattern, case=False, na=False)]

# Exclude words from Side_effects column
allergies = user_input['Allergies']
if allergies:
    allergy_pattern = '|'.join(allergies)
    filtered_drugs_db = filtered_drugs_db[~filtered_drugs_db['Side_effects'].str.contains(allergy_pattern, case=False, na=False)]

# User input to string
user_conditions = ' '.join([f'{k}:{v}' for k, v in user_input.items()])
print(user_conditions)

# Vectorize the drug descriptions
vectorizer = TfidfVectorizer()
drug_vectors = vectorizer.fit_transform(filtered_drugs_db['Uses'])
print("Drug Vectors:")
print(drug_vectors)

# Vectorize the user conditions
user_vector = vectorizer.transform([user_conditions])
print("User Vectors:")
print(user_vector)

# Cosine sim
similarity_scores = cosine_similarity(user_vector, drug_vectors).flatten()

# Recommend top 5 drugs
top_indices = similarity_scores.argsort()[:5][::-1]
recommended_drugs = filtered_drugs_db.iloc[top_indices]

print("Recommended Drugs:")
# for i in range(len(recommended_drugs)):
#     print(f"{i+1}. {recommended_drugs.iloc[i]['Medicine Name']}", ", ", f"{recommended_drugs.iloc[i]['Uses']}")
print(recommended_drugs[['Medicine Name', 'Uses', 'Side_effects']])
# print()


# 