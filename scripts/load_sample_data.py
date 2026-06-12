#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def create_sample_players_csv():
    """Crée un CSV d'exemple avec des joueurs"""
    data = {
        'name': ['Mohamed Salah', 'Vinicius Jr', 'Kylian Mbappe', 'Erling Haaland', 'Luis Diaz',
                 'Phil Foden', 'Bukayo Saka', 'Jude Bellingham', 'Alexis Mac Allister', 'Florian Wirtz'],
        'age': [32, 24, 25, 23, 27, 24, 23, 21, 25, 21],
        'nationality': ['Egyptian', 'Brazilian', 'French', 'Norwegian', 'Colombian',
                       'English', 'English', 'English', 'Argentine', 'German'],
        'position': ['RW', 'LW', 'ST', 'ST', 'LW', 'LW', 'RW', 'CM', 'CM', 'LW'],
        'club': ['Liverpool', 'Real Madrid', 'PSG', 'Manchester City', 'Liverpool',
                'Manchester City', 'Arsenal', 'Real Madrid', 'Liverpool', 'Bayer Leverkusen'],
        'league': ['Premier League', 'La Liga', 'Ligue 1', 'Premier League', 'Premier League',
                  'Premier League', 'Premier League', 'La Liga', 'Premier League', 'Bundesliga'],
        'market_value': [80000000, 95000000, 180000000, 180000000, 75000000,
                        120000000, 90000000, 150000000, 70000000, 100000000],
        'height': [175, 176, 178, 194, 180, 173, 178, 186, 179, 181],
        'foot': ['L', 'L', 'R', 'L', 'L', 'L', 'R', 'R', 'R', 'L']
    }
    
    df = pd.DataFrame(data)
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/players.csv', index=False)
    print(f"✅ Créé: data/raw/players.csv ({len(df)} joueurs)")
    return df

def create_sample_stats_csv():
    """Crée un CSV d'exemple avec les statistiques"""
    players = ['Mohamed Salah', 'Vinicius Jr', 'Kylian Mbappe', 'Erling Haaland', 'Luis Diaz',
               'Phil Foden', 'Bukayo Saka', 'Jude Bellingham', 'Alexis Mac Allister', 'Florian Wirtz']
    
    data = []
    for player in players:
        for season in ['2021-22', '2022-23', '2023-24']:
            data.append({
                'name': player,
                'season': season,
                'goals': np.random.randint(8, 25),
                'assists': np.random.randint(3, 12),
                'xg': np.random.uniform(8, 22),
                'xa': np.random.uniform(3, 10),
                'shots': np.random.randint(50, 180),
                'passes': np.random.randint(500, 2000),
                'passing_accuracy': np.random.uniform(75, 92),
                'pressing': np.random.randint(10, 40),
                'interceptions': np.random.randint(5, 25),
                'minutes_played': np.random.randint(1500, 2700)
            })
    
    df = pd.DataFrame(data)
    df.to_csv('data/raw/player_stats.csv', index=False)
    print(f"✅ Créé: data/raw/player_stats.csv ({len(df)} enregistrements)")
    return df

def create_sample_transfers_csv():
    """Crée un CSV d'exemple avec les transferts"""
    data = [
        {'player_name': 'Mohamed Salah', 'from_club': 'Chelsea', 'to_club': 'Liverpool', 
         'transfer_date': '2017-06-22', 'transfer_value': 45000000, 'transfer_type': 'permanent'},
        {'player_name': 'Kylian Mbappe', 'from_club': 'Monaco', 'to_club': 'PSG',
         'transfer_date': '2017-08-31', 'transfer_value': 180000000, 'transfer_type': 'permanent'},
        {'player_name': 'Erling Haaland', 'from_club': 'Borussia Dortmund', 'to_club': 'Manchester City',
         'transfer_date': '2023-06-15', 'transfer_value': 60000000, 'transfer_type': 'permanent'},
    ]
    
    df = pd.DataFrame(data)
    df.to_csv('data/raw/transfers.csv', index=False)
    print(f"✅ Créé: data/raw/transfers.csv ({len(df)} transferts)")
    return df

if __name__ == '__main__':
    print("📊 Création des données d'exemple...\n")
    create_sample_players_csv()
    create_sample_stats_csv()
    create_sample_transfers_csv()
    print("\n✅ Fichiers de données créés dans data/raw/")
    print("\n💡 Maintenant, exécutez:")
    print("   python scripts/run_pipeline.py")
