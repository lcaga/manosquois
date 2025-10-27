#!/usr/bin/env python3
"""
Création d'un package minimal avec seulement les fichiers essentiels
"""
import os
import zipfile
import base64
from datetime import datetime

def create_minimal_package():
    """Crée un package minimal avec les fichiers essentiels"""
    
    # Fichiers essentiels seulement
    essential_content = {
        'demo_app.html': open('demo_app.html', 'r', encoding='utf-8').read(),
        'app_simple.py': open('app_simple.py', 'r', encoding='utf-8').read(),
        'requirements.txt': open('requirements.txt', 'r', encoding='utf-8').read(),
        'README.md': """# Générateur de Documents SAS

## Démarrage Rapide
1. Ouvrez demo_app.html dans votre navigateur
2. Ou lancez: python3 app_simple.py

## Installation
```bash
pip install flask werkzeug requests
python3 app_simple.py
```

## Accès
- Interface démo: demo_app.html  
- Application: http://localhost:5000

Votre générateur de documents juridiques pour SAS est prêt !
""",
        'start.sh': """#!/bin/bash
echo "🚀 Démarrage du Générateur SAS"
pip install flask werkzeug requests --break-system-packages 2>/dev/null || pip install flask werkzeug requests
python3 app_simple.py
"""
    }
    
    # Créer le ZIP en mémoire
    zip_filename = "sas-generator-minimal.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename, content in essential_content.items():
            zipf.writestr(filename, content)
    
    print(f"✅ Package minimal créé: {zip_filename}")
    
    # Encoder en base64 pour affichage
    with open(zip_filename, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    
    return zip_filename, encoded

if __name__ == "__main__":
    zip_file, encoded_content = create_minimal_package()
    
    print(f"📦 Fichier: {zip_file}")
    print(f"📏 Taille: {len(encoded_content)} caractères encodés")
    
    # Sauvegarder le contenu encodé
    with open("package_encoded.txt", "w") as f:
        f.write(encoded_content)
    
    print("✅ Fichier encodé sauvegardé dans package_encoded.txt")