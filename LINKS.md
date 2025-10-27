# 🔗 Liens et Commandes Utiles

## 🌐 Accès à l'Application

### Interface Web Principale
```
http://localhost:5000
```

### Endpoints API
- **Test de santé** : `http://localhost:5000/test`
- **Upload de fichiers** : `POST http://localhost:5000/upload`
- **Extraction de données** : `POST http://localhost:5000/extract-data`
- **Génération de documents** : `POST http://localhost:5000/generate-documents`
- **Téléchargement** : `GET http://localhost:5000/download/{session_id}/{filename}`

## 🚀 Commandes de Lancement

### Démarrage Simple
```bash
./start.sh
```

### Démarrage Manuel
```bash
python3 app_simple.py
```

### Test Complet Automatisé
```bash
python3 test_demo.py
```

## 🔧 Commandes de Développement

### Installation des Dépendances de Base
```bash
pip install flask werkzeug requests --break-system-packages
```

### Installation Complète (pour version IA)
```bash
# Dépendances système
sudo apt-get install libreoffice tesseract-ocr tesseract-ocr-fra poppler-utils

# Environnement virtuel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Tests et Validation
```bash
# Test de santé
curl http://localhost:5000/test

# Test avec fichiers
curl -X POST \
  -F "kbis=@test_files/kbis.txt" \
  -F "statuts=@test_files/statuts.txt" \
  -F "comptes_n1=@test_files/comptes_n1.txt" \
  -F "comptes_n2=@test_files/comptes_n2.txt" \
  -F "comptes_n3=@test_files/comptes_n3.txt" \
  http://localhost:5000/upload

# Test extraction
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"files": {}}' \
  http://localhost:5000/extract-data
```

## 📁 Structure des Fichiers Importants

### Fichiers Principaux
- `app_simple.py` - Application de démonstration (ACTUELLE)
- `app.py` - Application complète avec IA
- `templates/index.html` - Interface utilisateur
- `static/style.css` - Design et styles
- `static/script.js` - Logique conversationnelle

### Fichiers de Configuration
- `config.py` - Configuration centralisée
- `requirements.txt` - Dépendances Python
- `start.sh` - Script de lancement

### Fichiers de Test
- `test_demo.py` - Tests automatisés
- `test_files/` - Fichiers d'exemple
- `generated/` - Documents générés

### Documentation
- `README.md` - Documentation technique
- `DEMO.md` - Guide de démonstration
- `SUCCESS.md` - Résumé du succès
- `LINKS.md` - Ce fichier de liens

## 📊 Monitoring et Debug

### Logs
```bash
# Logs en temps réel
tail -f app.log

# Statut des processus
ps aux | grep python3
```

### Arrêt de l'Application
```bash
# Arrêt propre
pkill -f "python3 app_simple.py"

# Arrêt forcé
pkill -9 -f "python3 app_simple.py"
```

### Nettoyage
```bash
# Nettoyer les fichiers générés
rm -rf generated/* uploads/*

# Nettoyer les tests
rm -f test_download_*
```

## 🎯 URLs de Test Rapide

### Validation Fonctionnelle
```bash
# Application fonctionne ?
curl -s http://localhost:5000/test | python3 -m json.tool

# Interface accessible ?
curl -s http://localhost:5000/ | head -5

# Test complet automatisé
python3 test_demo.py
```

---

## ✅ Application Prête !

L'application **Générateur de Documents SAS** est complètement fonctionnelle à l'adresse :

### 🌐 http://localhost:5000

Tous les tests passent avec succès et l'interface conversationnelle fonctionne parfaitement !