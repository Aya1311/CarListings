import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from mycar.models import Client, CarAvito, Sauvegarde, Visite
from sklearn.metrics import precision_score, recall_score

# Fonction pour obtenir les préférences d'un client
def get_client_preferences(user_id):
    client = Client.objects.get(user_id=user_id)
    preferences = {
        'carburant_prefere': client.carburant_prefere,
        'boite_preferee': client.boite_preferee,
        'budget_min': client.budget_min,
        'budget_max': client.budget_max,
    }
    return preferences

# Fonction pour obtenir les interactions d'un client
def get_client_interactions(user_id):
    client = Client.objects.get(user_id=user_id)
    sauvegardes = Sauvegarde.objects.filter(client_id=client.id)
    visites = Visite.objects.filter(client_id=client.id)
    saved_cars = [s.car for s in sauvegardes]
    visited_cars = [v.car for v in visites]
    return saved_cars, visited_cars

# Fonction pour préparer les données des voitures
def prepare_car_data():
    cars = CarAvito.objects.all()
    car_data = {
        'id_car': [car.id_car for car in cars],
        'title': [car.title for car in cars],
        'price': [car.price for car in cars],
        'carburant': [car.carburant for car in cars],
        'boite': [car.boite for car in cars],
        'puissance_fiscale': [car.puissance_fiscale for car in cars],
        'kilometrage': [car.kilometrage for car in cars],
        'year': [car.year for car in cars],
        'ville': [car.ville for car in cars],
        'image_url': [car.image_url for car in cars], 
    }
    return pd.DataFrame(car_data)

# Fonction pour calculer la similarité entre les voitures
def compute_similarity(cars_df):
    tfidf = TfidfVectorizer(stop_words='english')
    features = ['carburant', 'boite', 'puissance_fiscale', 'kilometrage', 'year', 'ville']
    cars_df['features'] = cars_df[features].fillna('').agg(' '.join, axis=1)
    tfidf_matrix = tfidf.fit_transform(cars_df['features'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Fonction pour appliquer les poids en fonction des préférences
def apply_preference_weights(car_df, preferences):
    weight_budget = 2  
    weight_carburant = 1
    weight_boite = 1
    
    car_df['score'] = 0  # Initialiser le score à 0
    car_df['score'] += weight_budget * ((car_df['price'] >= preferences['budget_min']) & (car_df['price'] <= preferences['budget_max']))
    car_df['score'] += weight_carburant * (car_df['carburant'] == preferences['carburant_prefere'])
    car_df['score'] += weight_boite * (car_df['boite'] == preferences['boite_preferee'])
    return car_df

# Fonction de recommandation de voitures
def recommend_cars(user_id):
    preferences = get_client_preferences(user_id)
    saved_cars, visited_cars = get_client_interactions(user_id)
    car_df = prepare_car_data()
    
    saved_car_ids = [car.id_car for car in saved_cars]
    visited_car_ids = [car.id_car for car in visited_cars]
    car_df = car_df[~car_df['id_car'].isin(saved_car_ids + visited_car_ids)]
    
    cosine_sim = compute_similarity(car_df)
    
    car_df['score'] = 0
    car_df['score'] += cosine_sim.mean(axis=0)
    
    # Appliquer les poids de préférence
    car_df = apply_preference_weights(car_df, preferences)

    recommendations = car_df.sort_values(by='score', ascending=False).head(10)
    return recommendations[['id_car', 'title', 'price', 'carburant', 'boite', 'puissance_fiscale', 'kilometrage', 'year', 'ville', 'image_url', 'score']]

# Fonction pour valider les recommandations
def validate_recommendations(user_id):
    # Obtenir les recommandations
    recommendations = recommend_cars(user_id)
    
    # Récupérer les voitures sauvegardées pour le client
    saved_cars, _ = get_client_interactions(user_id)
    saved_car_ids = [car.id_car for car in saved_cars]

    # Calculer les scores de précision et de rappel
    recommended_ids = recommendations['id_car'].tolist()
    
    # Générer des étiquettes pour les recommandations
    y_true = [1 if car_id in saved_car_ids else 0 for car_id in recommended_ids]
    y_pred = [1] * len(recommended_ids)  # Toutes les recommandations sont considérées comme positives

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)

    return precision, recall

# Exemple d'utilisation de la validation
user_id = 6  # Remplacez par l'ID d'un utilisateur spécifique
precision, recall = validate_recommendations(user_id)
print(f"Précision: {precision:.2f}, Rappel: {recall:.2f}")
