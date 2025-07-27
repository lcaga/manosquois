# 📦 IMPORT ET UTILISATION - Générateur Documents SAS

## 🎯 Instructions d'Importation dans Cursor

### 1. Téléchargement et Extraction
1. **Téléchargez** le fichier `generateur-sas-complet.zip`
2. **Décompressez** le fichier sur votre ordinateur
3. **Ouvrez Cursor**
4. **Menu** → "Fichier" → "Ouvrir le dossier" → Sélectionnez le dossier décompressé

### 2. Installation des Dépendances

#### Option A: Installation Automatique (Recommandée)
```bash
# Dans le terminal Cursor
chmod +x start.sh
./start.sh
```

#### Option B: Installation Manuelle
```bash
# Dépendances Python de base
pip install flask werkzeug requests

# Dépendances complètes (optionnel)
pip install -r requirements.txt
```

### 3. Démarrage de l'Application

#### Méthode 1: Script Automatique
```bash
./start.sh
```

#### Méthode 2: Démarrage Manuel
```bash
python3 app_simple.py
```

### 4. Accès à l'Application

#### Option A: Fichier HTML Direct (Plus Simple)
1. Ouvrez le fichier `demo_app.html` dans votre navigateur
2. L'interface complète s'affiche immédiatement

#### Option B: Serveur Web
1. Après démarrage, cherchez le port forwarding dans Cursor
2. Ou accédez à `http://localhost:5000` si disponible

## 🎯 Contenu du Package

### Fichiers Principaux
- **`app_simple.py`** - Application Flask simplifiée (prête à l'emploi)
- **`app.py`** - Application Flask complète avec IA
- **`demo_app.html`** - Interface de démonstration autonome

### Modules
- **`ai_extractor.py`** - Extraction de données avec IA
- **`document_generator.py`** - Génération de documents
- **`config.py`** - Configuration

### Interface
- **`templates/index.html`** - Interface web principale
- **`static/style.css`** - Styles modernes
- **`static/script.js`** - Logique conversationnelle

### Configuration
- **`requirements.txt`** - Dépendances Python
- **`README.md`** - Documentation complète

### Tests et Démo
- **`test_demo.py`** - Tests automatisés
- **`test_files/`** - Fichiers d'exemple
- **`access_app.py`** - Script de test d'accès

### Guides
- **`GUIDE_ACCES_SIMPLE.md`** - Guide d'accès simplifié
- **`QUICK_ACCESS.md`** - Accès rapide
- **`SUCCESS.md`** - Documentation du succès

## 🚀 Utilisation Rapide

### Scénario 1: Démonstration Immédiate
```bash
# Ouvrez demo_app.html dans votre navigateur
# L'interface s'affiche instantanément !
```

### Scénario 2: Application Complète
```bash
python3 app_simple.py
# Puis accédez via port forwarding ou localhost:5000
```

### Scénario 3: Test Automatisé
```bash
python3 test_demo.py
# Lance une démonstration complète
```

## 🔧 Fonctionnalités Incluses

✅ **Interface conversationnelle** complète  
✅ **Upload de fichiers** sécurisé  
✅ **Extraction de données** (simulation + IA)  
✅ **Génération de documents** automatique  
✅ **Templates Word** personnalisables  
✅ **Export PDF/DOCX**  
✅ **Design moderne** responsive  

## 🛠️ Personnalisation

### Ajouter votre clé OpenAI
```bash
# Dans config.py ou variable d'environnement
export OPENAI_API_KEY="votre-clé-ici"
```

### Modifier les templates
- Éditez les fichiers dans `templates/`
- Ajoutez vos propres templates Word

### Adapter l'interface
- Modifiez `static/style.css` pour le design
- Modifiez `static/script.js` pour la logique

## 🆘 Résolution de Problèmes

### L'application ne démarre pas
```bash
python3 access_app.py  # Diagnostic automatique
```

### Port 5000 occupé
```bash
python3 app_simple.py  # Utilise un port alternatif
```

### Dépendances manquantes
```bash
pip install flask werkzeug  # Minimum requis
```

## 📞 Support

- **Fichier de log** : Consultez les erreurs dans le terminal
- **Test de santé** : `curl http://localhost:5000/test`
- **Interface de démo** : Toujours disponible dans `demo_app.html`

---

🎉 **Votre Générateur de Documents SAS est prêt à être utilisé !**