"""
Version simplifiée de l'application pour tests sans dépendances lourdes
"""
import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
import tempfile
import shutil

# Configuration simple
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

# Créer les dossiers nécessaires
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Endpoint pour télécharger les fichiers"""
    try:
        uploaded_files = {}
        required_files = ['kbis', 'statuts', 'comptes_n1', 'comptes_n2', 'comptes_n3']
        
        for file_key in required_files:
            if file_key not in request.files:
                return jsonify({
                    'success': False,
                    'error': f'Fichier {file_key} manquant'
                }), 400
            
            file = request.files[file_key]
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': f'Aucun fichier sélectionné pour {file_key}'
                }), 400
            
            if file and allowed_file(file.filename):
                # Sécuriser le nom de fichier
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                # Sauvegarder le fichier
                file.save(file_path)
                uploaded_files[file_key] = {
                    'filename': filename,
                    'path': file_path,
                    'size': os.path.getsize(file_path)
                }
            else:
                return jsonify({
                    'success': False,
                    'error': f'Type de fichier non autorisé pour {file_key}'
                }), 400
        
        return jsonify({
            'success': True,
            'message': 'Fichiers téléchargés avec succès',
            'files': uploaded_files
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors du téléchargement: {str(e)}'
        }), 500

@app.route('/extract-data', methods=['POST'])
def extract_data():
    """Simulation de l'extraction de données"""
    try:
        data = request.get_json()
        files_info = data.get('files', {})
        
        # Simulation de l'extraction avec des données d'exemple
        extracted_data = {
            'kbis': {
                'denomination_sociale': 'EXEMPLE SAS',
                'capital_social': '10000',
                'adresse_siege': '123 Rue de la République, 75001 Paris',
                'numero_rcs': '123456789',
                'ville_greffe': 'Paris',
                'date_immatriculation': '2020-01-15'
            },
            'statuts': {
                'denomination_sociale': 'EXEMPLE SAS',
                'objet_social': 'Toutes activités commerciales',
                'duree_societe': '99 ans',
                'capital_social': '10000',
                'siege_social': '123 Rue de la République, 75001 Paris',
                'president': 'Jean DUPONT'
            },
            'comptes_n1': {
                'exercice': '2023',
                'chiffre_affaires': '150000',
                'resultat_net': '25000',
                'total_bilan': '75000'
            },
            'comptes_n2': {
                'exercice': '2022',
                'chiffre_affaires': '120000',
                'resultat_net': '18000',
                'total_bilan': '65000'
            },
            'comptes_n3': {
                'exercice': '2021',
                'chiffre_affaires': '100000',
                'resultat_net': '15000',
                'total_bilan': '55000'
            }
        }
        
        return jsonify({
            'success': True,
            'message': 'Données extraites avec succès',
            'extracted_data': extracted_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors de l\'extraction: {str(e)}'
        }), 500

@app.route('/generate-documents', methods=['POST'])
def generate_documents():
    """Simulation de la génération de documents"""
    try:
        data = request.get_json()
        form_data = data.get('form_data', {})
        extracted_data = data.get('extracted_data', {})
        
        # Simulation de la génération de documents
        session_id = str(uuid.uuid4())
        output_dir = os.path.join(app.config['GENERATED_FOLDER'], session_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # Créer des fichiers d'exemple
        generated_files = {
            'docx': [],
            'pdf': []
        }
        
        documents_to_generate = form_data.get('documents_choisis', ['convocation', 'pv_feuille'])
        
        for doc_type in documents_to_generate:
            # Créer un fichier texte d'exemple
            content = generate_sample_document_content(doc_type, form_data, extracted_data)
            
            # Version texte (simulant DOCX)
            txt_filename = f"{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            txt_path = os.path.join(output_dir, txt_filename)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            generated_files['docx'].append({
                'name': txt_filename,
                'path': txt_path,
                'type': doc_type
            })
        
        return jsonify({
            'success': True,
            'message': 'Documents générés avec succès',
            'generated_files': generated_files,
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erreur lors de la génération: {str(e)}'
        }), 500

def generate_sample_document_content(doc_type, form_data, extracted_data):
    """Génère le contenu d'un document d'exemple"""
    kbis_data = extracted_data.get('kbis', {})
    statuts_data = extracted_data.get('statuts', {})
    
    if doc_type == 'convocation':
        return f"""
CONVOCATION À L'ASSEMBLÉE GÉNÉRALE ORDINAIRE

{statuts_data.get('denomination_sociale', 'SOCIÉTÉ EXEMPLE')}
Société par Actions Simplifiée au capital de {kbis_data.get('capital_social', '10000')} euros
Siège social : {statuts_data.get('siege_social', 'Adresse du siège')}
Immatriculée au RCS de {kbis_data.get('ville_greffe', 'Paris')} sous le numéro {kbis_data.get('numero_rcs', 'XXX XXX XXX')}

Madame, Monsieur,

Nous avons l'honneur de vous convoquer à l'Assemblée Générale Ordinaire de la société {statuts_data.get('denomination_sociale', 'SOCIÉTÉ EXEMPLE')} qui se tiendra :

📅 DATE : {form_data.get('date_assemblee_generale', 'Date à définir')}
🕐 HEURE : {form_data.get('heure_assemblee_generale', 'Heure à définir')}
📍 LIEU : {form_data.get('lieu_assemblee_generale', 'Lieu à définir')}

ORDRE DU JOUR :

1. Approbation des comptes annuels de l'exercice clos le {form_data.get('date_cloture_exercice', 'Date de clôture')}
2. Affectation du résultat
3. Quitus aux dirigeants

Fait le {datetime.now().strftime('%d/%m/%Y')}

Le Président
{statuts_data.get('president', 'Président à définir')}
"""
    
    elif doc_type == 'pv_feuille':
        return f"""
PROCÈS-VERBAL D'ASSEMBLÉE GÉNÉRALE ORDINAIRE

{statuts_data.get('denomination_sociale', 'SOCIÉTÉ EXEMPLE')}
Société par Actions Simplifiée au capital de {kbis_data.get('capital_social', '10000')} euros
Siège social : {statuts_data.get('siege_social', 'Adresse du siège')}
Immatriculée au RCS de {kbis_data.get('ville_greffe', 'Paris')} sous le numéro {kbis_data.get('numero_rcs', 'XXX XXX XXX')}

L'an deux mille vingt-quatre et le {form_data.get('date_assemblee_generale', 'Date à définir')}, à {form_data.get('heure_assemblee_generale', 'Heure à définir')}, s'est réunie l'Assemblée Générale Ordinaire de la société {statuts_data.get('denomination_sociale', 'SOCIÉTÉ EXEMPLE')}, au {form_data.get('lieu_assemblee_generale', 'Lieu à définir')}.

Sont présents :
- {statuts_data.get('president', 'Président à définir')}, Président

ORDRE DU JOUR :

1. Approbation des comptes annuels de l'exercice clos le {form_data.get('date_cloture_exercice', 'Date de clôture')}
2. Affectation du résultat
3. Quitus aux dirigeants

RÉSOLUTIONS :

Première résolution - Approbation des comptes annuels
L'assemblée générale approuve les comptes annuels de l'exercice clos le {form_data.get('date_cloture_exercice', 'Date de clôture')}.
Cette résolution est adoptée à l'unanimité.

Deuxième résolution - Affectation du résultat
L'assemblée générale décide d'affecter le résultat selon les modalités proposées.
Cette résolution est adoptée à l'unanimité.

Troisième résolution - Quitus aux dirigeants
L'assemblée générale donne quitus aux dirigeants pour leur gestion.
Cette résolution est adoptée à l'unanimité.

L'ordre du jour étant épuisé et personne ne demandant plus la parole, la séance est levée.

Le Président
{statuts_data.get('president', 'Président à définir')}

FEUILLE DE PRÉSENCE

Nom et Prénom : {statuts_data.get('president', 'Président à définir')}
Qualité : Président
Signature : ________________
"""
    
    else:
        return f"Document de type {doc_type} - Contenu à définir"

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Télécharge un fichier généré"""
    try:
        file_path = os.path.join(app.config['GENERATED_FOLDER'], session_id, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Fichier non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test_endpoint():
    """Endpoint de test"""
    return jsonify({
        'status': 'OK',
        'message': 'Application fonctionnelle',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Démarrage de l'application Générateur de Documents SAS")
    print("📂 Dossiers créés :")
    print(f"   - Uploads: {UPLOAD_FOLDER}")
    print(f"   - Generated: {GENERATED_FOLDER}")
    print("🌐 Accès: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)