#!/usr/bin/env python3

import os
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.db_config import engine, Base
from src.database.models import *
from src.ml.pipeline import ScoutingPipeline
from src.utils.validators import DataValidator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_database():
    """Initialise la base de données"""
    logger.info("🗄️ Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Base de données initialisée")

def main():
    logger.info("="*60)
    logger.info("🚀 PIPELINE DE SCOUTING DE FOOTBALL")
    logger.info("="*60)
    
    initialize_database()
    
    logger.info("\n📂 Vérification des fichiers de données...")
    required_files = [
        'data/raw/players.csv',
        'data/raw/player_stats.csv',
        'data/raw/transfers.csv'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        logger.warning(f"Fichiers manquants: {missing_files}")
        logger.info("Création des données d'exemple...")
        os.system('python scripts/load_sample_data.py')
    
    logger.info("\n" + "="*60)
    pipeline = ScoutingPipeline()
    df_results, top_talents, underpriced = pipeline.run_from_csv()
    
    logger.info("\n💾 Sauvegarde des résultats...")
    os.makedirs('data/processed', exist_ok=True)
    
    df_results.to_csv('data/processed/players_with_predictions.csv', index=False)
    top_talents.to_csv('data/processed/top_talents.csv', index=False)
    underpriced.to_csv('data/processed/underpriced_talents.csv', index=False)
    
    logger.info("✅ Résultats sauvegardés dans data/processed/")
    
    logger.info("\n" + "="*60)
    logger.info("✅ PIPELINE TERMINÉ")
    logger.info("="*60)
    
    logger.info("\n📊 Fichiers générés:")
    logger.info("  - data/processed/players_with_predictions.csv")
    logger.info("  - data/processed/top_talents.csv")
    logger.info("  - data/processed/underpriced_talents.csv")
    logger.info("  - models/*.pkl (modèles ML)")
    
    logger.info("\n🎯 Prochaines étapes:")
    logger.info("  1. Lancer le Dashboard: python src/dashboard/app.py")
    logger.info("  2. Lancer l'API: python -m src.api.main")

if __name__ == '__main__':
    main()
