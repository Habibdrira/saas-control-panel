#!/bin/bash
set -e

echo "======================================"
echo "  Nettoyage final du projet SaaS"
echo "======================================"

# 0. Arrêter Docker Compose
echo "[1/8] Arrêt des containers Docker..."
docker compose down -v || true

# 1. Supprimer saas-app (microblog & anciens restes)
echo "[2/8] Suppression saas-app..."
rm -rf saas-app 2>/dev/null || true

# 2. Nettoyage auth-service
echo "[3/8] Nettoyage auth-service..."
rm -rf auth-service/venv 2>/dev/null || true

# 3. Nettoyage control-panel
echo "[4/8] Nettoyage control-panel..."
rm -rf control-panel/venv 2>/dev/null || true
rm -rf control-panel/app 2>/dev/null || true

# 4. Nettoyage user-dashboard
echo "[5/8] Nettoyage user-dashboard..."
rm -f user-dashboard/index.html 2>/dev/null || true
rm -rf user-dashboard/__pycache__ 2>/dev/null || true

# 5. Nettoyage fichiers temporaires Python
echo "[6/8] Suppression des fichiers temporaires Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# 6. Vérifier / corriger .gitignore
echo "[7/8] Mise à jour .gitignore..."
cat << 'GITEOF' > .gitignore
__pycache__/
*.pyc
.env
venv/
node_modules/
dist/
auth-service/users.db
GITEOF

# 7. Rebuild Docker (sans cache)
echo "[8/8] Rebuild Docker Compose..."
docker compose build --no-cache

echo "======================================"
echo "  Nettoyage terminé avec succès ✅"
echo "======================================"
