#!/usr/bin/env python3
"""
Script pour tester et accéder à l'application SAS
"""
import requests
import webbrowser
import time
import json
import sys

def test_app():
    """Test de l'application"""
    try:
        # Test de l'endpoint de santé
        response = requests.get("http://localhost:5000/test", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Application fonctionnelle !")
            print(f"📊 Status: {data['status']}")
            print(f"⏰ Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        print("🔧 Vérifiez que l'application est démarrée avec: python3 app_simple.py")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def show_access_info():
    """Affiche les informations d'accès"""
    print("\n" + "="*60)
    print("🌐 INFORMATIONS D'ACCÈS À VOTRE APPLICATION")
    print("="*60)
    print()
    print("🚀 Votre application est démarrée et fonctionne !")
    print()
    print("📍 URLs d'accès :")
    print("   • Interface principale: http://localhost:5000")
    print("   • Test de santé:        http://localhost:5000/test")
    print()
    print("🔧 Dans Cursor :")
    print("   1. Cherchez l'onglet 'Ports' ou 'Port Forwarding'")
    print("   2. Le port 5000 devrait être listé")
    print("   3. Cliquez sur le lien pour ouvrir dans votre navigateur")
    print()
    print("🔄 Alternative - Test en ligne de commande :")
    print("   curl http://localhost:5000")
    print()
    print("="*60)

def main():
    print("🔍 Test de l'application Générateur de Documents SAS...")
    print("-" * 60)
    
    if test_app():
        show_access_info()
        
        # Essayer d'ouvrir automatiquement
        try:
            print("\n🌐 Tentative d'ouverture automatique du navigateur...")
            webbrowser.open("http://localhost:5000")
            print("✅ Navigateur ouvert !")
        except Exception as e:
            print(f"⚠️  Impossible d'ouvrir automatiquement: {e}")
            
    else:
        print("\n🔧 Solutions de dépannage :")
        print("1. Redémarrez l'application: python3 app_simple.py")
        print("2. Vérifiez les processus: ps aux | grep app_simple")
        print("3. Vérifiez le port: curl http://localhost:5000/test")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())