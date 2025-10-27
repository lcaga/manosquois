import os
import json
import uuid
import subprocess
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import PyPDF2
from docxtpl import DocxTemplate
import openai
import tempfile
import shutil

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
GENERATED_FOLDER = 'generated'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

# Créer les dossiers nécessaires
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GENERATED_FOLDER'] = GENERATED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extrait le texte d'un PDF avec OCR si nécessaire"""
    try:
        # Essayer d'abord l'extraction directe
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Si peu de texte extrait, utiliser l'OCR
        if len(text.strip()) < 100:
            print("Peu de texte extrait, utilisation de l'OCR...")
            images = convert_from_path(file_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image, lang='fra')
        
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction de texte du PDF: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Extrait le texte d'un fichier Word"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction de texte du DOCX: {e}")
        return ""

def extract_data_with_ai(aggregated_text):
    """Utilise l'IA pour extraire les données structurées"""
    prompt = """Tu es un assistant expert en analyse de documents juridiques et comptables français. À partir du texte fourni ci-dessous, qui provient de l'extrait Kbis, des statuts et des comptes annuels d'une SAS, extrais les informations suivantes et formate-les exclusivement en JSON. Ignore toute information non pertinente.

- denomination_sociale_de_la_sas : Le nom complet de la société.
- montant_du_capital_social : Le capital social en chiffres et en euros.
- adresse_du_siege_social : L'adresse complète du siège social.
- ville_du_greffe_rcs : La ville du RCS où la société est immatriculée.
- numero_immatriculation_rcs : Le numéro SIREN/RCS unique.
- montant_resultat_benefice_ou_perte : Le résultat net (bénéfice ou perte) de l'exercice le plus récent disponible dans les comptes fournis, en précisant s'il s'agit d'un "bénéfice de X €" ou d'une "perte de Y €".
- nom_prenom_president_legal : Le nom et prénom du président légal de la société.

Voici le texte à analyser :
""" + aggregated_text + """

Ne produis que l'objet JSON en sortie."""

    try:
        # Configuration OpenAI (vous devrez définir votre clé API)
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY', 'your-api-key-here'))
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse de documents juridiques français."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        # Nettoyer la réponse pour extraire le JSON
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0]
        elif "```" in result:
            result = result.split("```")[1].split("```")[0]
        
        return json.loads(result.strip())
    except Exception as e:
        print(f"Erreur lors de l'extraction par IA: {e}")
        return {
            "denomination_sociale_de_la_sas": "",
            "montant_du_capital_social": "",
            "adresse_du_siege_social": "",
            "ville_du_greffe_rcs": "",
            "numero_immatriculation_rcs": "",
            "montant_resultat_benefice_ou_perte": "",
            "nom_prenom_president_legal": ""
        }

def convert_docx_to_pdf(docx_path, pdf_path):
    """Convertit un fichier DOCX en PDF"""
    try:
        # Utiliser LibreOffice en mode headless
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', os.path.dirname(pdf_path), docx_path
        ], check=True, capture_output=True)
        
        # Renommer le fichier si nécessaire
        base_name = os.path.splitext(os.path.basename(docx_path))[0]
        generated_pdf = os.path.join(os.path.dirname(pdf_path), f"{base_name}.pdf")
        if os.path.exists(generated_pdf) and generated_pdf != pdf_path:
            shutil.move(generated_pdf, pdf_path)
        
        return True
    except Exception as e:
        print(f"Erreur lors de la conversion PDF: {e}")
        try:
            # Fallback avec docx2pdf si LibreOffice échoue
            from docx2pdf import convert
            convert(docx_path, pdf_path)
            return True
        except Exception as e2:
            print(f"Erreur avec docx2pdf aussi: {e2}")
            return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_documents():
    try:
        # Vérifier les fichiers uploadés
        required_files = ['kbis', 'statuts', 'comptes_n1', 'comptes_n2', 'comptes_n3']
        uploaded_files = {}
        
        for file_key in required_files:
            if file_key not in request.files:
                return jsonify({'error': f'Fichier {file_key} manquant'}), 400
            
            file = request.files[file_key]
            if file.filename == '':
                return jsonify({'error': f'Aucun fichier sélectionné pour {file_key}'}), 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{file_key}_{uuid.uuid4().hex}_{file.filename}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files[file_key] = file_path
            else:
                return jsonify({'error': f'Type de fichier non autorisé pour {file_key}'}), 400
        
        # Extraire les données du formulaire
        form_data = {
            'date_cloture_exercice': request.form.get('date_cloture_exercice'),
            'date_assemblee_generale': request.form.get('date_assemblee_generale'),
            'heure_assemblee_generale': request.form.get('heure_assemblee_generale'),
            'lieu_assemblee_generale': request.form.get('lieu_assemblee_generale'),
            'nom_prenom_president_de_seance': request.form.get('nom_prenom_president_de_seance'),
            'nom_prenom_secretaire_de_seance': request.form.get('nom_prenom_secretaire_de_seance')
        }
        
        # Extraire le texte de tous les documents
        aggregated_text = ""
        for file_key, file_path in uploaded_files.items():
            if file_path.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            elif file_path.lower().endswith(('.docx', '.doc')):
                text = extract_text_from_docx(file_path)
            else:
                continue
            
            aggregated_text += f"\n=== {file_key.upper()} ===\n{text}\n"
        
        # Extraire les données avec l'IA
        extracted_data = extract_data_with_ai(aggregated_text)
        
        # Fusionner les données extraites avec les données du formulaire
        context = {**extracted_data, **form_data}
        
        # Formater la date pour l'affichage
        if context.get('date_assemblee_generale'):
            date_obj = datetime.strptime(context['date_assemblee_generale'], '%Y-%m-%d')
            context['date_assemblee_generale_formatee'] = date_obj.strftime('%d %B %Y')
        
        # Générer un ID unique pour cette génération
        generation_id = uuid.uuid4().hex
        
        # Créer les modèles (vous devrez les placer dans le dossier templates)
        templates = {
            'pv_feuille': 'PV + Feuille de présence.docx',
            'convocation': 'Convocation à l\'AG des associés.docx'
        }
        
        generated_files = {}
        
        for doc_type, template_name in templates.items():
            template_path = os.path.join('templates', template_name)
            
            if not os.path.exists(template_path):
                print(f"Template {template_path} non trouvé, création d'un template de base")
                # Créer un template de base si le fichier n'existe pas
                continue
            
            # Générer le document Word
            doc_template = DocxTemplate(template_path)
            doc_template.render(context)
            
            docx_filename = f"{doc_type}_{generation_id}.docx"
            docx_path = os.path.join(app.config['GENERATED_FOLDER'], docx_filename)
            doc_template.save(docx_path)
            
            # Générer le PDF
            pdf_filename = f"{doc_type}_{generation_id}.pdf"
            pdf_path = os.path.join(app.config['GENERATED_FOLDER'], pdf_filename)
            
            if convert_docx_to_pdf(docx_path, pdf_path):
                generated_files[f"{doc_type}_docx"] = docx_filename
                generated_files[f"{doc_type}_pdf"] = pdf_filename
            else:
                generated_files[f"{doc_type}_docx"] = docx_filename
                generated_files[f"{doc_type}_pdf"] = None
        
        # Nettoyer les fichiers uploadés
        for file_path in uploaded_files.values():
            try:
                os.remove(file_path)
            except:
                pass
        
        return jsonify({
            'success': True,
            'files': generated_files,
            'extracted_data': extracted_data
        })
        
    except Exception as e:
        print(f"Erreur lors de la génération: {e}")
        return jsonify({'error': f'Erreur lors de la génération: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['GENERATED_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Fichier non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': f'Erreur lors du téléchargement: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)