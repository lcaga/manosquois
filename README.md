# Générateur de Documents Juridiques pour SAS

Application web pour automatiser la génération de documents juridiques pour les Assemblées Générales de SAS françaises.

## 🎯 Fonctionnalités

- **Interface conversationnelle** : Assistant chatbot pour guider l'utilisateur
- **Extraction automatique** : Analyse des documents avec IA (OCR inclus)
- **Génération multi-format** : Documents Word et PDF
- **Design moderne** : Interface responsive et épurée

## 📋 Prérequis

### Système
- Python 3.8+
- LibreOffice (pour la conversion PDF)
- Tesseract OCR (pour l'extraction de texte des images)

### Sur Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install libreoffice tesseract-ocr tesseract-ocr-fra poppler-utils
```

### Sur macOS
```bash
brew install libreoffice tesseract tesseract-lang poppler
```

### Sur Windows
1. Installer LibreOffice : https://www.libreoffice.org/download/download/
2. Installer Tesseract : https://github.com/UB-Mannheim/tesseract/wiki
3. Installer Poppler : https://blog.alivate.com.au/poppler-windows/

## 🚀 Installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd generateur-documents-sas
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration de l'API OpenAI**
```bash
export OPENAI_API_KEY="votre-clé-api-openai"
# Sur Windows: set OPENAI_API_KEY=votre-clé-api-openai
```

5. **Créer les modèles Word**
Placez vos modèles de documents dans le dossier `templates/` :
- `PV + Feuille de présence.docx`
- `Convocation à l'AG des associés.docx`

## 📄 Modèles de Documents

Les modèles Word doivent utiliser la syntaxe Jinja2 avec les variables suivantes :

### Variables extraites automatiquement :
- `{{ denomination_sociale_de_la_sas }}`
- `{{ montant_du_capital_social }}`
- `{{ adresse_du_siege_social }}`
- `{{ ville_du_greffe_rcs }}`
- `{{ numero_immatriculation_rcs }}`
- `{{ montant_resultat_benefice_ou_perte }}`
- `{{ nom_prenom_president_legal }}`

### Variables saisies par l'utilisateur :
- `{{ date_cloture_exercice }}`
- `{{ date_assemblee_generale }}`
- `{{ date_assemblee_generale_formatee }}` (format français)
- `{{ heure_assemblee_generale }}`
- `{{ lieu_assemblee_generale }}`
- `{{ nom_prenom_president_de_seance }}`
- `{{ nom_prenom_secretaire_de_seance }}`

### Exemple de modèle :
```
ASSEMBLÉE GÉNÉRALE ORDINAIRE
{{ denomination_sociale_de_la_sas }}

Date : {{ date_assemblee_generale_formatee }}
Heure : {{ heure_assemblee_generale }}
Lieu : {{ lieu_assemblee_generale }}

Président de séance : {{ nom_prenom_president_de_seance }}
Secrétaire : {{ nom_prenom_secretaire_de_seance }}
```

## 🏃‍♂️ Lancement

```bash
python app.py
```

L'application sera accessible sur : http://localhost:5000

## 📁 Structure du Projet

```
generateur-documents-sas/
├── app.py                 # Serveur Flask principal
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── templates/            # Modèles HTML et Word
│   ├── index.html       # Interface principale
│   ├── PV + Feuille de présence.docx
│   └── Convocation à l'AG des associés.docx
├── static/               # Fichiers statiques
│   ├── style.css        # Styles CSS
│   └── script.js        # JavaScript
├── uploads/              # Fichiers temporaires uploadés
└── generated/            # Documents générés
```

## 🔧 Utilisation

1. **Téléchargement des documents** :
   - Extrait Kbis (< 3 mois)
   - Statuts de la société
   - Comptes annuels N-1, N-2, N-3

2. **Interface conversationnelle** :
   - Date de clôture d'exercice
   - Date et heure de l'AG
   - Lieu de l'assemblée
   - Président et secrétaire de séance

3. **Génération automatique** :
   - Documents Word (.docx)
   - Documents PDF (.pdf)

## 🔒 Sécurité

- Les fichiers uploadés sont supprimés après traitement
- Validation des types de fichiers
- Limite de taille des fichiers (50MB)
- Noms de fichiers sécurisés

## 🛠️ Dépannage

### Erreur LibreOffice
```bash
# Vérifier l'installation
libreoffice --version
# Tester la conversion
libreoffice --headless --convert-to pdf test.docx
```

### Erreur Tesseract
```bash
# Vérifier l'installation
tesseract --version
# Tester OCR
tesseract image.png output.txt -l fra
```

### Erreur OpenAI
- Vérifiez votre clé API
- Vérifiez votre quota/crédit
- Testez avec une requête simple

## 📝 Notes Importantes

- **Clé API OpenAI** : Nécessaire pour l'extraction automatique des données
- **Templates** : Doivent être placés dans le dossier `templates/`
- **Formats supportés** : PDF, DOCX, DOC
- **OCR** : Automatic pour les PDFs scannés
- **Validation** : Contrainte de 6 mois pour la date d'AG

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou problème :
- Créer une issue sur GitHub
- Vérifier les logs dans la console
- Consulter la documentation des dépendances