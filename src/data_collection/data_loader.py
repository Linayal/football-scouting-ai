import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from src.database.models import Player, PlayerStats, Club, Transfer, Injury
from src.database.db_config import SessionLocal
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
    
    def load_players_from_csv(self, csv_path: str):
        """Charge les joueurs depuis un fichier CSV"""
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Chargement de {len(df)} joueurs")
            
            for idx, row in df.iterrows():
                existing = self.db.query(Player).filter(Player.name == row['name']).first()
                if existing:
                    continue
                
                club = self.db.query(Club).filter(Club.name == row.get('club', 'Unknown')).first()
                if not club:
                    club = Club(
                        name=row.get('club', 'Unknown'),
                        country=row.get('club_country', 'Unknown'),
                        league=row.get('league', 'Unknown')
                    )
                    self.db.add(club)
                    self.db.commit()
                
                player = Player(
                    name=row['name'],
                    age=int(row['age']) if pd.notna(row['age']) else None,
                    nationality=row.get('nationality', 'Unknown'),
                    position=row.get('position', 'Unknown'),
                    current_club_id=club.id,
                    market_value=float(row['market_value']) if pd.notna(row['market_value']) else 0,
                    height=row.get('height', None),
                    foot=row.get('foot', None)
                )
                self.db.add(player)
            
            self.db.commit()
            logger.info("✅ Joueurs chargés avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des joueurs: {e}")
            self.db.rollback()
    
    def load_player_stats_from_csv(self, csv_path: str):
        """Charge les statistiques des joueurs"""
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Chargement de {len(df)} enregistrements de stats")
            
            for idx, row in df.iterrows():
                if 'player_id' in row and pd.notna(row['player_id']):
                    player = self.db.query(Player).filter(Player.id == row['player_id']).first()
                else:
                    player = self.db.query(Player).filter(Player.name == row.get('name', '')).first()
                
                if not player:
                    continue
                
                existing = self.db.query(PlayerStats).filter(
                    PlayerStats.player_id == player.id,
                    PlayerStats.season == row['season']
                ).first()
                
                if existing:
                    continue
                
                stats = PlayerStats(
                    player_id=player.id,
                    season=row['season'],
                    goals=float(row.get('goals', 0)),
                    assists=float(row.get('assists', 0)),
                    xg=float(row.get('xg', 0)),
                    xa=float(row.get('xa', 0)),
                    shots=float(row.get('shots', 0)),
                    passes=float(row.get('passes', 0)),
                    passing_accuracy=float(row.get('passing_accuracy', 0)),
                    pressing=float(row.get('pressing', 0)),
                    interceptions=float(row.get('interceptions', 0)),
                    minutes_played=float(row.get('minutes_played', 0))
                )
                self.db.add(stats)
            
            self.db.commit()
            logger.info("✅ Statistiques chargées avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des stats: {e}")
            self.db.rollback()
    
    def get_all_players_with_stats(self) -> pd.DataFrame:
        """Retourne un DataFrame avec tous les joueurs et leurs dernières stats"""
        from sqlalchemy import text
        query = text("""
        SELECT 
            p.id, p.name, p.age, p.position, p.nationality, p.market_value,
            c.name as club, c.league,
            ps.season, ps.goals, ps.assists, ps.xg, ps.xa, ps.shots, 
            ps.passes, ps.passing_accuracy, ps.pressing, ps.interceptions, ps.minutes_played
        FROM players p
        LEFT JOIN clubs c ON p.current_club_id = c.id
        LEFT JOIN player_stats ps ON p.id = ps.player_id
        ORDER BY p.name, ps.season DESC
        """)
        
        result = self.db.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        
        return df
