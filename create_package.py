#!/usr/bin/env python3
"""
Script pour créer un package téléchargeable de l'application SAS
"""
import os
import shutil
import zipfile
from datetime import datetime

def create_package():
    """Crée un package ZIP téléchargeable avec tous les fichiers nécessaires"""
    
    package_name = "generateur-sas-complet"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Créer le dossier temporaire pour le package
    temp_dir = f"{package_name}_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # Fichiers essentiels à inclure
    essential_files = [
        # Applications principales
        "app_simple.py",
        "app.py",
        "demo_app.html",
        
        # Modules Python
        "ai_extractor.py", 
        "document_generator.py",
        "config.py",
        
        # Configuration
        "requirements.txt",
        "start.sh",
        
        # Documentation
        "README.md",
        "INSTRUCTIONS_IMPORT.md",
        "GUIDE_ACCES_SIMPLE.md",
        "QUICK_ACCESS.md",
        "SUCCESS.md",
        "COMMENT_VOIR_MON_APP.txt",
        "LINKS.md",
        
        # Scripts utiles
        "test_demo.py",
        "access_app.py",
        "app_test_local.py",
    ]
    
    # Dossiers à inclure
    essential_dirs = [
        "templates",
        "static", 
        "test_files"
    ]
    
    print(f"📦 Création du package {package_name}...")
    print("=" * 50)
    
    # Copier les fichiers essentiels
    copied_files = 0
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, temp_dir)
            print(f"✅ Copié: {file}")
            copied_files += 1
        else:
            print(f"⚠️  Fichier manquant: {file}")
    
    # Copier les dossiers essentiels
    copied_dirs = 0
    for dir_name in essential_dirs:
        if os.path.exists(dir_name):
            dest_dir = os.path.join(temp_dir, dir_name)
            shutil.copytree(dir_name, dest_dir)
            print(f"✅ Copié dossier: {dir_name}/")
            copied_dirs += 1
        else:
            print(f"⚠️  Dossier manquant: {dir_name}")
    
    # Créer les dossiers vides nécessaires
    empty_dirs = ["uploads", "generated"]
    for dir_name in empty_dirs:
        dir_path = os.path.join(temp_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        # Créer un fichier .gitkeep pour maintenir le dossier
        with open(os.path.join(dir_path, ".gitkeep"), "w") as f:
            f.write("# Dossier maintenu pour l'application\n")
        print(f"✅ Créé dossier: {dir_name}/")
    
    # Créer un fichier de version
    version_info = f"""# Générateur de Documents SAS
Version: 1.0.0
Date de création: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Fichiers inclus: {copied_files}
Dossiers inclus: {copied_dirs + len(empty_dirs)}

## Démarrage Rapide
1. Ouvrez demo_app.html dans votre navigateur
2. Ou lancez: python3 app_simple.py

## Documentation
- INSTRUCTIONS_IMPORT.md - Guide d'importation
- GUIDE_ACCES_SIMPLE.md - Accès simplifié
- README.md - Documentation complète
"""
    
    with open(os.path.join(temp_dir, "VERSION.txt"), "w", encoding="utf-8") as f:
        f.write(version_info)
    
    # Créer le fichier ZIP
    zip_filename = f"{package_name}.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
    
    print(f"\n📁 Création de l'archive {zip_filename}...")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Chemin relatif dans le ZIP (sans le dossier temporaire)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
                
    # Nettoyer le dossier temporaire
    shutil.rmtree(temp_dir)
    
    # Informations finales
    file_size = os.path.getsize(zip_filename) / 1024 / 1024  # MB
    
    print("=" * 50)
    print("🎉 PACKAGE CRÉÉ AVEC SUCCÈS !")
    print("=" * 50)
    print(f"📦 Nom du fichier: {zip_filename}")
    print(f"📏 Taille: {file_size:.2f} MB")
    print(f"📁 Chemin complet: {os.path.abspath(zip_filename)}")
    print(f"📊 Fichiers inclus: {copied_files}")
    print(f"📂 Dossiers inclus: {copied_dirs + len(empty_dirs)}")
    print()
    print("🚀 Instructions pour l'utilisateur:")
    print("1. Téléchargez le fichier ZIP")
    print("2. Décompressez-le sur votre ordinateur")
    print("3. Ouvrez le dossier dans Cursor")
    print("4. Lancez: python3 app_simple.py")
    print("5. Ou ouvrez demo_app.html dans votre navigateur")
    print()
    print("✅ Le package est prêt à être distribué !")
    
    return zip_filename

if __name__ == "__main__":
    try:
        zip_file = create_package()
        print(f"\n📥 Fichier téléchargeable créé: {zip_file}")
    except Exception as e:
        print(f"❌ Erreur lors de la création du package: {e}")
        import traceback
        traceback.print_exc()