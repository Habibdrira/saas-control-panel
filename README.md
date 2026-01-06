# SaaS Docker Control Panel

## 📌 Présentation
Ce projet est une plateforme SaaS qui crée automatiquement
un container Docker dédié pour chaque utilisateur inscrit.

## 🏗️ Architecture
- Microblog (Flask) : application SaaS utilisateur
- Control Panel (Flask) : API d’orchestration Docker
- Docker Engine : isolation par container

## 🔄 Fonctionnement
1. L’utilisateur s’inscrit sur Microblog
2. Microblog appelle l’API du Control Panel
3. Un container Docker est créé automatiquement
4. L’utilisateur dispose de son instance dédiée

## ⚙️ Technologies
- Python / Flask
- Docker SDK
- REST API
- Linux (Ubuntu)

## ▶️ Lancement

### Control Panel
```bash
cd control-panel
source venv/bin/activate
export CONTROL_PANEL_API_KEY=super-secret-key
python3 run.py

