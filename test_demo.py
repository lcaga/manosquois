#!/usr/bin/env python3
"""
Script de test et démonstration pour l'application SAS
"""
import requests
import json
import time
import os

# Configuration
BASE_URL = "http://localhost:5000"
TEST_FILES = {
    'kbis': 'test_files/kbis.txt',
    'statuts': 'test_files/statuts.txt',
    'comptes_n1': 'test_files/comptes_n1.txt',
    'comptes_n2': 'test_files/comptes_n2.txt',
    'comptes_n3': 'test_files/comptes_n3.txt'
}

def test_health():
    """Test de l'endpoint de santé"""
    print("🏥 Test de santé de l'application...")
    try:
        response = requests.get(f"{BASE_URL}/test")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Application fonctionnelle: {data['message']}")
            return True
        else:
            print(f"❌ Erreur: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Impossible de se connecter: {e}")
        return False

def test_upload():
    """Test du téléchargement de fichiers"""
    print("\n📁 Test de téléchargement des fichiers...")
    
    files = {}
    try:
        for key, file_path in TEST_FILES.items():
            if os.path.exists(file_path):
                files[key] = open(file_path, 'rb')
            else:
                print(f"❌ Fichier manquant: {file_path}")
                return None
        
        response = requests.post(f"{BASE_URL}/upload", files=files)
        
        # Fermer les fichiers
        for f in files.values():
            f.close()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Fichiers téléchargés: {data['message']}")
            return data.get('files', {})
        else:
            print(f"❌ Erreur upload: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement: {e}")
        return None

def test_extraction(files_info):
    """Test de l'extraction de données"""
    print("\n🔍 Test d'extraction de données...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/extract-data",
            json={'files': files_info},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Extraction réussie: {data['message']}")
            
            # Afficher quelques données extraites
            extracted = data.get('extracted_data', {})
            if 'kbis' in extracted:
                kbis = extracted['kbis']
                print(f"   📋 Société: {kbis.get('denomination_sociale', 'N/A')}")
                print(f"   💰 Capital: {kbis.get('capital_social', 'N/A')} euros")
            
            return extracted
        else:
            print(f"❌ Erreur extraction: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return None

def test_generation(files_info, extracted_data):
    """Test de génération de documents"""
    print("\n📄 Test de génération de documents...")
    
    # Données du formulaire de test
    form_data = {
        'date_cloture_exercice': '2023-12-31',
        'date_assemblee_generale': '2024-06-15',
        'heure_assemblee_generale': '14h00',
        'lieu_assemblee_generale': 'Au siège social',
        'documents_choisis': ['convocation', 'pv_feuille'],
        'approbation_comptes': True,
        'affectation_resultat': 'Report à nouveau',
        'quitus_dirigeants': True
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate-documents",
            json={
                'form_data': form_data,
                'extracted_data': extracted_data
            },
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération réussie: {data['message']}")
            
            # Afficher les fichiers générés
            generated = data.get('generated_files', {})
            session_id = data.get('session_id')
            
            if 'docx' in generated:
                print(f"   📄 Documents générés:")
                for doc in generated['docx']:
                    print(f"      - {doc['name']} ({doc['type']})")
                    
            return session_id, generated
        else:
            print(f"❌ Erreur génération: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return None, None

def test_download(session_id, generated_files):
    """Test de téléchargement des documents générés"""
    print("\n⬇️  Test de téléchargement des documents...")
    
    if not session_id or not generated_files:
        print("❌ Pas de fichiers à télécharger")
        return False
    
    try:
        for doc in generated_files.get('docx', []):
            filename = doc['name']
            url = f"{BASE_URL}/download/{session_id}/{filename}"
            
            response = requests.get(url)
            if response.status_code == 200:
                # Sauvegarder le fichier dans le dossier de test
                test_download_path = f"test_download_{filename}"
                with open(test_download_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Téléchargé: {test_download_path}")
            else:
                print(f"❌ Erreur téléchargement {filename}: {response.status_code}")
                
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement: {e}")
        return False

def run_full_demo():
    """Lance la démonstration complète"""
    print("🚀 DÉMONSTRATION COMPLÈTE - Générateur de Documents SAS")
    print("=" * 60)
    
    # Test 1: Santé de l'application
    if not test_health():
        print("❌ L'application n'est pas accessible. Vérifiez qu'elle fonctionne sur le port 5000.")
        return False
    
    # Test 2: Upload des fichiers
    files_info = test_upload()
    if not files_info:
        print("❌ Échec du téléchargement des fichiers.")
        return False
    
    # Test 3: Extraction des données
    extracted_data = test_extraction(files_info)
    if not extracted_data:
        print("❌ Échec de l'extraction des données.")
        return False
    
    # Test 4: Génération des documents
    session_id, generated_files = test_generation(files_info, extracted_data)
    if not session_id:
        print("❌ Échec de la génération des documents.")
        return False
    
    # Test 5: Téléchargement
    if not test_download(session_id, generated_files):
        print("❌ Échec du téléchargement.")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 DÉMONSTRATION TERMINÉE AVEC SUCCÈS !")
    print("\n📋 Résumé:")
    print("   ✅ Application fonctionnelle")
    print("   ✅ Téléchargement de fichiers")
    print("   ✅ Extraction de données (simulation)")
    print("   ✅ Génération de documents")
    print("   ✅ Téléchargement des résultats")
    print("\n🌐 Interface web disponible sur: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    run_full_demo()