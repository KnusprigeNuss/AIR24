import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

drugs_db = pd.read_csv('../../data/Medicine_Details.csv')

# Test user
user_input = {
    'Smoking': 'Yes',
    'Stroke': 'Yes',
    'Alcohol': 'No',
    'Diabetes': 'Yes',
    'Gender': 'Male',
    'Age': 0,
    'Cholesterol': 200,
    'BloodPressure': 120,
    'PhysicalActivity': 3,
    'BMI': 28.5,
    'PhysicalHealth': 5,
    'MentalHealth': 3,
    'Allergies': ['penicillin', 'aspirin', 'Diarrhea', 'Bupropion']  
}

# User to df
user_df = pd.DataFrame([user_input])

# Filter conditions for dataset
conditions = []
if user_input['Smoking'] == 'Yes':
    conditions.append('smoking')
if user_input['Stroke'] == 'Yes':
    conditions.append('stroke')
if user_input['Alcohol'] == 'Yes':
    conditions.append('alcohol')
if user_input['Diabetes'] == 'Yes':
    conditions.append('diabetes')

# Filter dataset
filtered_drugs_db = drugs_db[drugs_db['Uses'].str.contains('|'.join(conditions), case=False, na=False)]
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
top_indices = similarity_scores.argsort()[:][::-1]
recommended_drugs = filtered_drugs_db.iloc[top_indices]

print("Recommended Drugs:")
# for i in range(len(recommended_drugs)):
#     print(f"{i+1}. {recommended_drugs.iloc[i]['Medicine Name']}", ", ", f"{recommended_drugs.iloc[i]['Uses']}")
print(recommended_drugs[['Medicine Name', 'Uses', 'Side_effects']])
# print()


# 