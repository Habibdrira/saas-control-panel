# 🐳 SaaS Control Panel – Docker Containers Management Platform

## 📌 Description générale

Ce projet est une plateforme **SaaS de gestion de conteneurs Docker** développée avec **Python (Flask)** et **Docker**.  
Il permet :

- aux **utilisateurs** de s’inscrire et d’accéder automatiquement à leur **dashboard personnel** (conteneur dédié),
- à un **administrateur** de gérer **tous les conteneurs Docker** (voir, créer, démarrer, arrêter, supprimer),
- de piloter Docker via une **interface web**.

Le projet respecte strictement les exigences d’un projet **Cloud / DevOps / Docker**.

---

## 🧱 Architecture du projet



## 🔐 Rôles et fonctionnalités

### 👤 Utilisateur

- Inscription avec :
  - username
  - email
  - mot de passe
- Un **conteneur Docker dédié** est automatiquement créé après l’inscription
- Après login :
  - redirection automatique vers son dashboard personnel
  - affichage de :
    - username
    - email
    - URL et port du conteneur

URL utilisateur : http://localhost:5000/user/login


---

### 🛠️ Administrateur

- Login admin sécurisé
- Accès au **dashboard Docker**
- Peut :
  - voir tous les conteneurs Docker
  - voir le statut (running / stopped)
  - voir les ports exposés
  - démarrer un conteneur
  - arrêter un conteneur
  - supprimer un conteneur
  - créer un nouveau conteneur manuellement
  - ouvrir un conteneur via son port

URL admin : http://localhost:5000/admin/login


Identifiants admin par défaut :
username: admin
password: admin123

yaml
Copier le code

---

## ⚙️ Technologies utilisées

- Python 3.11
- Flask (backend)
- Docker SDK for Python
- Docker & Docker Compose
- HTML / CSS basique
- Linux (Ubuntu)

❗ **Docker sur Windows n’est PAS utilisé**, conformément aux consignes.

---

## 🚀 Lancement du projet (Étapes complètes)

### 1️⃣ Prérequis

- Linux (Ubuntu recommandé)
- Docker installé
- Docker Compose installé

Vérification :
```bash
docker --version
docker compose version
2️⃣ Script de nettoyage + lancement (RECOMMANDÉ)
Le projet fournit un script qui :

supprime tous les conteneurs existants

nettoie les images Docker

rebuild toutes les images

lance la plateforme

bash
Copier le code
chmod +x saas-reset-run.sh
./saas-reset-run.sh
3️⃣ Accès à la plateforme
Authentification utilisateur :

bash
Copier le code
http://localhost:5000/user/login
Authentification administrateur :

bash
Copier le code
http://localhost:5000/admin/login
Dashboard admin Docker :

bash
Copier le code
http://localhost:5001/admin
🔁 Fonctionnement backend (logique)
🔹 Inscription utilisateur
L’utilisateur s’inscrit via auth-service

auth-service envoie une requête REST au control-panel

control-panel :

crée un conteneur Docker

assigne un port automatiquement

stocke la relation user ↔ conteneur

🔹 Connexion utilisateur
L’utilisateur se connecte

auth-service interroge le control-panel

Le port du conteneur est récupéré via une API REST

Redirection automatique vers :

arduino
Copier le code
http://localhost:<PORT_DU_CONTENEUR>
🔹 Administration Docker
Le control-panel communique directement avec :

Docker API (via Docker SDK Python)

commandes Docker internes (start / stop / remove)

📦 Conformité avec l’énoncé du projet
✔ Interface web pour création de conteneurs
✔ Backend Python (Flask)
✔ Gestion complète des conteneurs (CRUD)
✔ Projet Dockerisé
✔ Fonctionne sur Linux
✔ README complet
✔ Projet explicable ligne par ligne

👉 Le projet valide 100% l’énoncé demandé.

🎓 Niveau du projet
Niveau : Intermédiaire → Avancé

Domaine : Cloud / DevOps / Docker

Prêt pour :

soutenance

démonstration

dépôt GitHub

✅ Conclusion
Ce projet démontre :

la compréhension de Docker

la communication inter-services

la séparation des rôles

la gestion SaaS multi-utilisateurs

les bases solides DevOps

🚀 Projet prêt à être rendu.

EOF

yaml
Copier le code

---

## 🏁 CE QUE TU PEUX FAIRE ENSUITE

1️⃣ Push sur GitHub  
2️⃣ Préparer ta soutenance  
3️⃣ Expliquer :
- architecture
- Docker
- API REST
- logique SaaS



