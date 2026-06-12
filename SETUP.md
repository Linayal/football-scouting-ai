# 🚀 Guide de Démarrage - AI Football Scouting Platform

## 1️⃣ Prérequis

- Python 3.9+
- PostgreSQL
- Git

## 2️⃣ Installation Locale

### Étape 1: Cloner le repo
```bash
git clone https://github.com/Linayal/football-scouting-ai.git
cd football-scouting-ai
```

### Étape 2: Créer un environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Étape 3: Installer les dépendances
```bash
pip install -r requirements.txt
```

## 3️⃣ Configuration Base de Données

### Option A: PostgreSQL Local

1. Installer PostgreSQL: https://www.postgresql.org/download/
2. Créer la base de données:
```bash
createdb football_scouting
```

3. Configurer `.env`:
```bash
cp .env.example .env
```

4. Éditer `.env`:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/football_scouting
```

### Option B: Docker (Plus facile)

Créer `docker-compose.yml`:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: football_scouting
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Lancer:
```bash
docker-compose up -d
```

## 4️⃣ Initialiser la Base de Données

```bash
python -c "
from src.database.db_config import engine, Base
from src.database.models import *

Base.metadata.create_all(bind=engine)
print('✅ Tables créées avec succès!')
"
```

## 5️⃣ Configuration API Keys (Optionnel)

Pour l'IA générative, ajouter à `.env`:

```env
# OpenAI
OPENAI_API_KEY=sk-...

# Cohere
COHERE_API_KEY=...
```

Obtenir les clés:
- OpenAI: https://platform.openai.com/api-keys
- Cohere: https://cohere.com/

## 6️⃣ Démarrer les Services

### Démarrer l'API FastAPI
```bash
python -m src.api.main
# Accès: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Démarrer le Dashboard Dash (autre terminal)
```bash
python src/dashboard/app.py
# Accès: http://localhost:8050
```

### Démarrer le pipeline complet (optionnel)
```bash
python main.py
```

## 7️⃣ Charger les Données

### Option 1: Web Scraping (LENT - 30min+)
```python
python -c "
from src.data_collection.transfermarkt_scraper import TransfermarktScraper
from src.data_collection.fbref_scraper import FBrefScraper

# Scraper Transfermarkt
tm = TransfermarktScraper()
# tm.scrape_player_data('url')

# Scraper FBref
fbref = FBrefScraper()
# data = fbref.scrape_league_stats('EPL', '2023-2024')
print('Scraping lancé...')
"
```

### Option 2: Fichiers CSV (RAPIDE)
Placer vos fichiers CSV dans `data/raw/`:
- `players.csv`
- `player_stats.csv`
- `transfers.csv`

Puis charger:
```python
python -c "
import pandas as pd
from src.database.db_config import SessionLocal
from src.database.models import Player, PlayerStats

players_df = pd.read_csv('data/raw/players.csv')
stats_df = pd.read_csv('data/raw/player_stats.csv')

# Charger dans la DB
db = SessionLocal()
# ... code pour insérer ...
print('✅ Données chargées!')
"
```

## 8️⃣ Tester l'API

### Obtenir les talents
```bash
curl http://localhost:8000/talent-discovery/top?limit=20
```

### Trouver des joueurs similaires
```bash
curl -X POST http://localhost:8000/players/similar \
  -H "Content-Type: application/json" \
  -d '{"player_name": "Salah", "n_results": 10}'
```

### Docs interactive
Aller à: http://localhost:8000/docs

## 9️⃣ Structure des Fichiers CSV

### `players.csv`
```
name,age,nationality,position,club,market_value,height,foot
Mohamed Salah,32,Egyptian,RW,Liverpool,60000000,175,L
```

### `player_stats.csv`
```
player_id,season,goals,assists,xg,xa,shots,minutes_played
1,2023-24,18,8,15.2,6.5,120,2700
```

### `transfers.csv`
```
player_id,from_club,to_club,transfer_date,transfer_value,transfer_type
1,Chelsea,Liverpool,2021-06-01,45000000,permanent
```

## 🔟 Troubleshooting

### Erreur: `ModuleNotFoundError`
```bash
pip install -r requirements.txt --upgrade
```

### Erreur: Base de données non trouvée
```bash
# Vérifier la connexion
python -c "
from src.database.db_config import engine
print(engine.url)
"
```

### Erreur: Port 5432 déjà utilisé
```bash
# Changer le port dans .env:
DATABASE_URL=postgresql://user:pass@localhost:5433/db
```

### Erreur: Pas de module LLM
```bash
pip install openai cohere
```

## 1️⃣1️⃣ Commandes Utiles

### Nettoyer les tables
```bash
python -c "
from src.database.db_config import engine, Base
from src.database.models import *

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print('✅ Reset complet!')
"
```

### Vérifier les données
```bash
python -c "
from src.database.db_config import SessionLocal
from src.database.models import Player

db = SessionLocal()
players = db.query(Player).limit(5).all()
for p in players:
    print(f'{p.name} - {p.age} ans - {p.position}')
"
```

### Générer un rapport PDF
```bash
python -c "
from src.reporting.pdf_report import PDFReportGenerator

pdf = PDFReportGenerator('reports/report.pdf')
pdf.add_title('Test Report')
pdf.add_section('Title', 'Content here')
pdf.add_footer()
pdf.generate()
print('✅ PDF généré!')
"
```

## 1️⃣2️⃣ Prochaines Étapes

1. ✅ Setup complet (ci-dessus)
2. 📊 Charger les données
3. 🤖 Entraîner les modèles ML
4. 📈 Visualiser sur le Dashboard
5. 📄 Générer les rapports PDF
6. 🚀 Déployer (Heroku, AWS, etc.)

## 1️⃣3️⃣ Ressources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Dash Plotly](https://dash.plotly.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [XGBoost](https://xgboost.readthedocs.io/)
- [UMAP](https://umap-learn.readthedocs.io/)

---

**Besoin d'aide ?** Ouvre une issue sur GitHub!
