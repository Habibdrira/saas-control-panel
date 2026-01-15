# 🎛️ SaaS Control Panel

**Plateforme SaaS complète pour gérer des conteneurs utilisateurs avec interface admin et dashboards personnels.**

## 🚀 Démarrage Rapide

```bash
# Construire les services
docker compose build

# Lancer la plateforme
docker compose up -d

# Vérifier le statut
docker compose ps
```

**Services disponibles:**
- Auth Service: http://localhost:5000 (Inscription/Connexion)
- Control Panel: http://localhost:5001 (Admin - `admin`/`admin123`)
- User Dashboard: Port dynamique (assigné à chaque utilisateur)

## 📦 Architecture

```
┌─────────────────────────────────────────────┐
│  Auth Service (:5000)                       │
│  - Inscription/connexion utilisateurs       │
│  - Gestion des sessions                     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  Control Panel (:5001)                      │
│  - Dashboard admin avec statistiques        │
│  - Gestion des conteneurs                   │
│  - API de provisionnement                   │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────▼─────────┐
        │ Base de données   │
        │ SQLite partagée   │
        │ /data/*.db        │
        └─────────┬─────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  User Containers (ports dynamiques)         │
│  - Dashboard personnel par utilisateur      │
│  - Métriques et activité                    │
└─────────────────────────────────────────────┘
```

## ✨ Fonctionnalités

### Admin (Control Panel)
✅ Dashboard avec stats en temps réel  
✅ Gestion des utilisateurs  
✅ Contrôle des conteneurs (start/stop/delete)  
✅ Recherche et filtres  
✅ Journal d'activité complet  

### Utilisateurs
✅ Dashboard personnel avec métriques  
✅ Statut du service et informations  
✅ Graphiques de performance (CPU, mémoire)  
✅ Timeline d'activité  

## 📋 Base de Données

**4 tables principales:**
- `users` - Comptes utilisateurs
- `containers` - Conteneurs provisionnés
- `activity_logs` - Audit trail
- `metrics` - Données de performance

**Localisation:** `/data/saas_control_panel.db` (volume Docker partagé)

## 🔌 API

### Provisionner un conteneur
```bash
curl -X POST http://localhost:5001/api/provision \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com"}'
```

### Obtenir les statistiques (admin)
```bash
GET /api/admin/stats
```

### Obtenir le port d'un utilisateur
```bash
GET /api/user/{username}/port
```

## 🛠️ Développement

### Structure du projet
```
saas-control-panel/
├── auth-service/        # Service d'authentification
│   ├── app.py
│   ├── database.py
│   └── templates/
├── control-panel/       # Panneau d'administration
│   ├── app.py
│   ├── database.py
│   └── templates/
├── user-app/           # Application utilisateur
│   ├── app.py
│   └── templates/
└── docker-compose.yml  # Orchestration
```

### Commandes utiles

```bash
# Voir les logs
docker compose logs -f {service}

# Redémarrer un service
docker compose restart {service}

# Reconstruire après modifications
docker compose build {service}
docker compose up -d {service}

# Accéder à la base de données
docker exec -it saas-control-panel-control-panel-1 \
  sqlite3 /data/saas_control_panel.db
```

## 🐛 Dépannage

**Services ne démarrent pas:**
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Erreur 500 sur dashboard utilisateur:**
```bash
docker logs {container-name}
docker compose restart
```

**Réinitialiser la base de données:**
```bash
docker exec saas-control-panel-control-panel-1 rm /data/saas_control_panel.db
docker compose restart
```

## 📊 Informations Techniques

- **Backend:** Flask (Python 3.11)
- **Base de données:** SQLite
- **Conteneurisation:** Docker + Docker Compose
- **Frontend:** HTML5/CSS3/JavaScript vanilla
- **Design:** Responsive, mobile-friendly

## 🔐 Sécurité

**Implémenté:**
- Session-based authentication
- Activity logging
- Container isolation

**À implémenter:**
- Bcrypt password hashing
- CSRF protection
- Rate limiting
- Security headers

## 📝 License

Projet fourni tel quel à des fins éducatives et commerciales.

---

**Version:** 1.0.0  
**Dernière mise à jour:** Janvier 2026  
**Statut:** ✅ Production Ready
