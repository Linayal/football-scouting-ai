import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle
import logging
from src.ml.market_value_prediction import MarketValuePredictor
from src.ml.career_prediction import CareerPredictor
from src.ml.clustering import PlayerClustering
from src.ml.similarity import PlayerSimilarity
from src.features.engineering import FeatureEngineer
import os

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, models_path: str = "models"):
        self.models_path = models_path
        os.makedirs(models_path, exist_ok=True)
        self.trained_models = {}
    
    def prepare_player_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prépare les données des joueurs pour le ML"""
        logger.info("Préparation des données...")
        
        df = df.sort_values('season', na_position='last').drop_duplicates('name', keep='last')
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        fe = FeatureEngineer()
        df = fe.create_per90_features(df)
        df = fe.create_ratio_features(df)
        df = fe.create_advanced_features(df)
        
        logger.info(f"✅ {len(df)} joueurs prêts pour le ML")
        return df
    
    def train_market_value_model(self, df: pd.DataFrame, model_type: str = 'xgboost'):
        """Entraîne le modèle de prédiction de valeur marchande"""
        logger.info(f"Entraînement du modèle de valeur marchande ({model_type})...")
        
        try:
            predictor = MarketValuePredictor(model_type=model_type)
            X_train, X_test, y_train, y_test = predictor.prepare_data(df)
            
            if model_type == 'xgboost':
                predictor.train_xgboost(X_train, y_train, X_test, y_test)
            elif model_type == 'lightgbm':
                predictor.train_lightgbm(X_train, y_train, X_test, y_test)
            elif model_type == 'catboost':
                predictor.train_catboost(X_train, y_train, X_test, y_test)
            
            model_path = os.path.join(self.models_path, f'market_value_{model_type}.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(predictor, f)
            
            logger.info(f"✅ Modèle sauvegardé: {model_path}")
            logger.info(f"Métriques: {predictor.metrics}")
            
            self.trained_models['market_value'] = predictor
            return predictor
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement: {e}")
            return None
    
    def train_clustering_model(self, df: pd.DataFrame, method: str = 'kmeans', n_clusters: int = 5):
        """Entraîne le modèle de clustering de joueurs"""
        logger.info(f"Entraînement du clustering ({method}, {n_clusters} clusters)...")
        
        try:
            feature_cols = [
                'goals_per90', 'assists_per90', 'xg_per90', 'xa_per90',
                'passing_accuracy', 'interceptions_per90', 'pressing_per90'
            ]
            
            available_cols = [col for col in feature_cols if col in df.columns]
            X = df[available_cols].fillna(0).values
            
            clusterer = PlayerClustering(n_clusters=n_clusters)
            
            if method == 'kmeans':
                clusters = clusterer.kmeans_clustering(X)
            elif method == 'hdbscan':
                clusters = clusterer.hdbscan_clustering(X)
            else:
                clusters = clusterer.kmeans_clustering(X)
            
            embedding = clusterer.reduce_dimensions(X)
            
            model_path = os.path.join(self.models_path, f'clustering_{method}.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(clusterer, f)
            
            logger.info(f"✅ Clustering sauvegardé: {model_path}")
            
            df['cluster'] = clusters
            df['umap_x'] = embedding[:, 0]
            df['umap_y'] = embedding[:, 1]
            
            self.trained_models['clustering'] = clusterer
            return df, clusterer
            
        except Exception as e:
            logger.error(f"Erreur lors du clustering: {e}")
            return None, None
    
    def train_similarity_model(self, df: pd.DataFrame):
        """Entraîne le modèle de similarité de joueurs"""
        logger.info("Entraînement du modèle de similarité...")
        
        try:
            feature_cols = [
                'goals_per90', 'assists_per90', 'xg_per90', 'xa_per90',
                'passing_accuracy', 'interceptions_per90', 'pressing_per90',
                'shot_accuracy'
            ]
            
            available_cols = [col for col in feature_cols if col in df.columns]
            X = df[available_cols].fillna(0).values
            
            similarity = PlayerSimilarity(n_neighbors=10)
            similarity.fit(X, df.reset_index(drop=True))
            
            model_path = os.path.join(self.models_path, 'similarity.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(similarity, f)
            
            logger.info(f"✅ Modèle de similarité sauvegardé: {model_path}")
            
            self.trained_models['similarity'] = similarity
            return similarity
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement de similarité: {e}")
            return None
    
    def train_all_models(self, df: pd.DataFrame):
        """Entraîne tous les modèles"""
        logger.info("="*50)
        logger.info("🤖 ENTRAÎNEMENT DE TOUS LES MODÈLES")
        logger.info("="*50)
        
        df_prepared = self.prepare_player_data(df)
        
        self.train_market_value_model(df_prepared, 'xgboost')
        df_prepared, _ = self.train_clustering_model(df_prepared, 'kmeans', 5)
        self.train_similarity_model(df_prepared)
        
        logger.info("="*50)
        logger.info("✅ TOUS LES MODÈLES ENTRAÎNÉS")
        logger.info("="*50)
        
        return df_prepared
    
    def load_model(self, model_name: str, model_type: str = None):
        """Charge un modèle sauvegardé"""
        if model_type:
            model_path = os.path.join(self.models_path, f'{model_name}_{model_type}.pkl')
        else:
            model_path = os.path.join(self.models_path, f'{model_name}.pkl')
        
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"✅ Modèle chargé: {model_path}")
            return model
        else:
            logger.warning(f"Modèle non trouvé: {model_path}")
            return None
