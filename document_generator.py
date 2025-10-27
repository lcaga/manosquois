"""
Module de génération de documents à partir de templates Word
"""
import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, List
from docxtpl import DocxTemplate
import tempfile
import shutil

class DocumentGenerator:
    def __init__(self, templates_folder: str = "templates"):
        """Initialise le générateur avec le dossier des templates"""
        self.templates_folder = templates_folder
        
        # Templates disponibles
        self.available_templates = {
            'convocation': 'Convocation à l\'AG des associés.docx',
            'pv_feuille': 'PV + Feuille de présence.docx',
            'pv_seul': 'PV d\'AG seul.docx',
            'rapport_gestion': 'Rapport de gestion.docx'
        }
    
    def format_date_french(self, date_str: str) -> str:
        """Formate une date au format français"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            mois = [
                'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
            ]
            return f"{date_obj.day} {mois[date_obj.month - 1]} {date_obj.year}"
        except:
            return date_str
    
    def format_currency(self, amount: str) -> str:
        """Formate un montant en euros"""
        try:
            # Nettoyer le montant
            clean_amount = ''.join(filter(str.isdigit, str(amount)))
            if clean_amount:
                amount_int = int(clean_amount)
                return f"{amount_int:,}".replace(',', ' ') + " euros"
            return str(amount)
        except:
            return str(amount)
    
    def prepare_template_data(self, form_data: Dict[str, Any], extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prépare les données pour les templates"""
        
        # Données de base depuis les documents
        kbis_data = extracted_data.get('kbis', {})
        statuts_data = extracted_data.get('statuts', {})
        comptes_n1 = extracted_data.get('comptes_n1', {})
        comptes_n2 = extracted_data.get('comptes_n2', {})
        comptes_n3 = extracted_data.get('comptes_n3', {})
        
        # Consolidation des données
        template_data = {
            # Informations société (priorité aux statuts, puis Kbis)
            'denomination_sociale_de_la_sas': (
                statuts_data.get('denomination_sociale') or 
                kbis_data.get('denomination_sociale') or 
                'À COMPLÉTER'
            ),
            'montant_du_capital_social': self.format_currency(
                statuts_data.get('capital_social') or 
                kbis_data.get('capital_social') or 
                '0'
            ),
            'adresse_du_siege_social': (
                statuts_data.get('siege_social') or 
                kbis_data.get('adresse_siege') or 
                'À COMPLÉTER'
            ),
            'numero_immatriculation_rcs': (
                kbis_data.get('numero_rcs') or 
                'À COMPLÉTER'
            ),
            'ville_du_greffe_rcs': (
                kbis_data.get('ville_greffe') or 
                'À COMPLÉTER'
            ),
            
            # Données de l'assemblée depuis le formulaire
            'date_assemblee_generale': form_data.get('date_assemblee_generale', ''),
            'date_assemblee_generale_formatee': self.format_date_french(
                form_data.get('date_assemblee_generale', '')
            ),
            'heure_assemblee_generale': form_data.get('heure_assemblee_generale', ''),
            'lieu_assemblee_generale': form_data.get('lieu_assemblee_generale', ''),
            'date_cloture_exercice': form_data.get('date_cloture_exercice', ''),
            'date_cloture_exercice_formatee': self.format_date_french(
                form_data.get('date_cloture_exercice', '')
            ),
            
            # Données financières
            'chiffre_affaires_n1': self.format_currency(
                comptes_n1.get('chiffre_affaires', '0')
            ),
            'resultat_net_n1': self.format_currency(
                comptes_n1.get('resultat_net', '0')
            ),
            'total_bilan_n1': self.format_currency(
                comptes_n1.get('total_bilan', '0')
            ),
            'chiffre_affaires_n2': self.format_currency(
                comptes_n2.get('chiffre_affaires', '0')
            ),
            'resultat_net_n2': self.format_currency(
                comptes_n2.get('resultat_net', '0')
            ),
            'chiffre_affaires_n3': self.format_currency(
                comptes_n3.get('chiffre_affaires', '0')
            ),
            'resultat_net_n3': self.format_currency(
                comptes_n3.get('resultat_net', '0')
            ),
            
            # Dirigeants
            'president_sas': (
                statuts_data.get('president') or 
                'À COMPLÉTER'
            ),
            
            # Résolutions (depuis le formulaire)
            'resolutions': form_data.get('resolutions', []),
            'approbation_comptes': form_data.get('approbation_comptes', True),
            'affectation_resultat': form_data.get('affectation_resultat', ''),
            'quitus_dirigeants': form_data.get('quitus_dirigeants', True),
            'autres_resolutions': form_data.get('autres_resolutions', []),
            
            # Informations complémentaires
            'duree_societe': statuts_data.get('duree_societe', '99 ans'),
            'objet_social': statuts_data.get('objet_social', 'À COMPLÉTER'),
            
            # Dates formatées pour l'affichage
            'date_du_jour': datetime.now().strftime('%d/%m/%Y'),
            'annee_exercice': form_data.get('date_cloture_exercice', '')[:4] if form_data.get('date_cloture_exercice') else '',
        }
        
        return template_data
    
    def generate_document(self, template_name: str, data: Dict[str, Any], output_path: str) -> bool:
        """Génère un document à partir d'un template"""
        try:
            template_path = os.path.join(self.templates_folder, self.available_templates[template_name])
            
            if not os.path.exists(template_path):
                print(f"Template non trouvé: {template_path}")
                return False
            
            # Charger le template
            doc = DocxTemplate(template_path)
            
            # Remplir avec les données
            doc.render(data)
            
            # Sauvegarder
            doc.save(output_path)
            
            print(f"Document généré: {output_path}")
            return True
            
        except Exception as e:
            print(f"Erreur lors de la génération de {template_name}: {e}")
            return False
    
    def convert_to_pdf(self, docx_path: str, pdf_path: str) -> bool:
        """Convertit un fichier Word en PDF"""
        try:
            # Utiliser LibreOffice pour la conversion
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(pdf_path),
                docx_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Renommer le fichier si nécessaire
                base_name = os.path.splitext(os.path.basename(docx_path))[0]
                temp_pdf = os.path.join(os.path.dirname(pdf_path), f"{base_name}.pdf")
                
                if os.path.exists(temp_pdf) and temp_pdf != pdf_path:
                    shutil.move(temp_pdf, pdf_path)
                
                return os.path.exists(pdf_path)
            else:
                print(f"Erreur LibreOffice: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Erreur conversion PDF: {e}")
            return False
    
    def generate_all_documents(self, form_data: Dict[str, Any], extracted_data: Dict[str, Any], output_dir: str) -> Dict[str, List[str]]:
        """Génère tous les documents demandés"""
        
        # Préparer les données pour les templates
        template_data = self.prepare_template_data(form_data, extracted_data)
        
        # Créer le dossier de sortie
        os.makedirs(output_dir, exist_ok=True)
        
        generated_files = {'docx': [], 'pdf': []}
        
        # Documents à générer selon les choix de l'utilisateur
        documents_to_generate = form_data.get('documents_choisis', ['convocation', 'pv_feuille'])
        
        for doc_type in documents_to_generate:
            if doc_type in self.available_templates:
                
                # Générer la version Word
                docx_filename = f"{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
                docx_path = os.path.join(output_dir, docx_filename)
                
                if self.generate_document(doc_type, template_data, docx_path):
                    generated_files['docx'].append(docx_path)
                    
                    # Générer la version PDF
                    pdf_filename = f"{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    pdf_path = os.path.join(output_dir, pdf_filename)
                    
                    if self.convert_to_pdf(docx_path, pdf_path):
                        generated_files['pdf'].append(pdf_path)
        
        return generated_files
    
    def create_sample_templates(self):
        """Crée des templates d'exemple si ils n'existent pas"""
        
        sample_templates = {
            'convocation': {
                'filename': 'Convocation à l\'AG des associés.docx',
                'content': """
CONVOCATION À L'ASSEMBLÉE GÉNÉRALE ORDINAIRE

{{ denomination_sociale_de_la_sas }}
Société par Actions Simplifiée au capital de {{ montant_du_capital_social }}
Siège social : {{ adresse_du_siege_social }}
Immatriculée au RCS de {{ ville_du_greffe_rcs }} sous le numéro {{ numero_immatriculation_rcs }}

Madame, Monsieur,

Nous avons l'honneur de vous convoquer à l'Assemblée Générale Ordinaire de la société {{ denomination_sociale_de_la_sas }} qui se tiendra :

📅 DATE : {{ date_assemblee_generale_formatee }}
🕐 HEURE : {{ heure_assemblee_generale }}
📍 LIEU : {{ lieu_assemblee_generale }}

ORDRE DU JOUR :

{% if approbation_comptes %}
1. Approbation des comptes annuels de l'exercice clos le {{ date_cloture_exercice_formatee }}
{% endif %}

{% if affectation_resultat %}
2. Affectation du résultat : {{ affectation_resultat }}
{% endif %}

{% if quitus_dirigeants %}
3. Quitus aux dirigeants
{% endif %}

{% for resolution in autres_resolutions %}
{{ loop.index + 3 }}. {{ resolution }}
{% endfor %}

Fait à {{ lieu_assemblee_generale }}, le {{ date_du_jour }}

Le Président
                """
            }
        }
        
        # Créer les templates d'exemple si le dossier templates existe
        if not os.path.exists(self.templates_folder):
            os.makedirs(self.templates_folder)
            
        for template_name, template_info in sample_templates.items():
            template_path = os.path.join(self.templates_folder, template_info['filename'])
            if not os.path.exists(template_path):
                # Pour une vraie application, il faudrait créer des vrais fichiers .docx
                # Ici on crée juste un fichier texte pour l'exemple
                with open(template_path.replace('.docx', '_example.txt'), 'w', encoding='utf-8') as f:
                    f.write(template_info['content'])
                    
                print(f"Template d'exemple créé: {template_path.replace('.docx', '_example.txt')}")