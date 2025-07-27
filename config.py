"""
Configuration de l'application
"""
import os

class Config:
    # Clés API
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    
    # Dossiers
    UPLOAD_FOLDER = 'uploads'
    GENERATED_FOLDER = 'generated'
    TEMPLATES_FOLDER = 'templates'
    
    # Extensions autorisées
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
    
    # Taille maximale des fichiers (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuration de debug
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'yes']
    
    # Langues supportées pour OCR
    OCR_LANGUAGES = 'fra+eng'
    
    # Templates disponibles
    AVAILABLE_TEMPLATES = {
        'convocation': {
            'name': 'Convocation à l\'AG des associés',
            'filename': 'Convocation à l\'AG des associés.docx',
            'description': 'Document de convocation pour l\'assemblée générale'
        },
        'pv_feuille': {
            'name': 'PV + Feuille de présence',
            'filename': 'PV + Feuille de présence.docx',
            'description': 'Procès-verbal avec feuille de présence intégrée'
        },
        'pv_seul': {
            'name': 'PV d\'AG seul',
            'filename': 'PV d\'AG seul.docx',
            'description': 'Procès-verbal simple sans feuille de présence'
        },
        'rapport_gestion': {
            'name': 'Rapport de gestion',
            'filename': 'Rapport de gestion.docx',
            'description': 'Rapport de gestion pour l\'assemblée générale'
        }
    }
    
    # Messages d'erreur
    ERROR_MESSAGES = {
        'file_too_large': 'Le fichier est trop volumineux (maximum 16MB)',
        'invalid_extension': 'Extension de fichier non autorisée',
        'upload_failed': 'Échec du téléchargement du fichier',
        'extraction_failed': 'Échec de l\'extraction des données',
        'generation_failed': 'Échec de la génération des documents',
        'missing_files': 'Fichiers requis manquants',
        'invalid_data': 'Données du formulaire invalides'
    }
    
    # Configuration par défaut pour les suggestions
    DEFAULT_SUGGESTIONS = {
        'heures_ag': ['09h00', '10h00', '11h00', '14h00', '15h00', '16h00', '17h00'],
        'lieux_ag': [
            'Au siège social',
            'En visioconférence',
            'Dans les locaux de l\'expert-comptable',
            'Chez le président',
            'En cabinet d\'avocat'
        ],
        'affectation_resultat': [
            'Report à nouveau',
            'Distribution en dividendes',
            'Mise en réserve',
            'Apurement des pertes antérieures'
        ],
        'autres_resolutions': [
            'Approbation des conventions réglementées',
            'Renouvellement du mandat du commissaire aux comptes',
            'Modification des statuts',
            'Autorisation de cautions, avals et garanties'
        ]
    }

# Configuration pour l'environnement de développement
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

# Configuration pour l'environnement de production
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

# Configuration pour les tests
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = 'test_uploads'
    GENERATED_FOLDER = 'test_generated'

# Choisir la configuration selon l'environnement
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}