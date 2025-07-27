#!/usr/bin/env python3
"""
Générateur de Documents SAS - Application Complète
Version autonome pour débutants
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-change-in-production'

# Créer les dossiers nécessaires
os.makedirs('uploads', exist_ok=True)
os.makedirs('generated', exist_ok=True)

# Template HTML intégré
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Générateur de Documents SAS</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #718096;
            font-weight: 400;
        }
        
        .section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .section h2 {
            color: #2d3748;
            margin-bottom: 25px;
            font-size: 1.8rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .upload-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .upload-item {
            padding: 20px;
            border: 2px dashed #cbd5e0;
            border-radius: 10px;
            text-align: center;
            transition: all 0.3s ease;
            background: rgba(247, 250, 252, 0.5);
        }
        
        .upload-item:hover {
            border-color: #667eea;
            background: rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        
        .upload-item label {
            display: block;
            font-weight: 600;
            margin-bottom: 10px;
            color: #4a5568;
        }
        
        .upload-item input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: white;
        }
        
        .chat-container {
            background: #f7fafc;
            border-radius: 15px;
            padding: 20px;
            max-height: 500px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 12px;
            max-width: 70%;
            animation: fadeInUp 0.3s ease;
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-right: auto;
        }
        
        .user-message {
            background: #e2e8f0;
            color: #2d3748;
            margin-left: auto;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .status-banner {
            background: #48bb78;
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            font-weight: 600;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .chat-input {
            width: 100%;
            padding: 12px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            font-size: 16px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Générateur de Documents pour Assemblée Générale de SAS</h1>
            <p class="subtitle">Automatisation de la génération de documents juridiques</p>
        </header>

        <div class="status-banner">
            ✅ Application Fonctionnelle - {{ timestamp }}
        </div>

        <!-- Section 1: Téléchargement des documents -->
        <section id="upload-section" class="section">
            <h2>📁 Documents requis</h2>
            <div class="upload-grid">
                <div class="upload-item">
                    <label for="kbis">📄 Extrait Kbis (moins de 3 mois)</label>
                    <input type="file" id="kbis" name="kbis" accept=".pdf,.docx,.doc">
                </div>
                <div class="upload-item">
                    <label for="statuts">📜 Statuts de la société à jour</label>
                    <input type="file" id="statuts" name="statuts" accept=".pdf,.docx,.doc">
                </div>
                <div class="upload-item">
                    <label for="comptes_n1">📊 Comptes annuels N-1</label>
                    <input type="file" id="comptes_n1" name="comptes_n1" accept=".pdf,.docx,.doc">
                </div>
                <div class="upload-item">
                    <label for="comptes_n2">📊 Comptes annuels N-2</label>
                    <input type="file" id="comptes_n2" name="comptes_n2" accept=".pdf,.docx,.doc">
                </div>
                <div class="upload-item">
                    <label for="comptes_n3">📊 Comptes annuels N-3</label>
                    <input type="file" id="comptes_n3" name="comptes_n3" accept=".pdf,.docx,.doc">
                </div>
            </div>
            <button class="btn" onclick="uploadFiles()">📤 Télécharger les documents</button>
        </section>

        <!-- Section 2: Assistant conversationnel -->
        <section id="chat-section" class="section">
            <h2>💬 Assistant Conversationnel</h2>
            <div class="chat-container" id="chat-messages">
                <!-- Les messages apparaîtront ici -->
            </div>
        </section>
    </div>

    <script>
        // Variables globales
        let currentStep = 0;
        let formData = {};
        
        // Questions de l'assistant
        const questions = [
            {
                question: "Pour commencer, quelle est la date de clôture de l'exercice comptable que vous souhaitez approuver ?",
                type: 'date',
                field: 'date_cloture_exercice'
            },
            {
                question: "Parfait. Quand souhaitez-vous tenir votre Assemblée Générale ?",
                type: 'date',
                field: 'date_assemblee_generale'
            },
            {
                question: "À quelle heure se tiendra l'assemblée ?",
                type: 'time',
                field: 'heure_assemblee_generale'
            },
            {
                question: "Où se déroulera l'Assemblée Générale ?",
                type: 'text',
                field: 'lieu_assemblee_generale'
            },
            {
                question: "Quel est le montant de la rémunération que vous souhaitez vous allouer en tant que dirigeant ?",
                type: 'number',
                field: 'remuneration_dirigeant'
            }
        ];
        
        function addMessage(text, sender, isInput = false) {
            const chatContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            if (isInput) {
                messageDiv.innerHTML = `
                    <div>${text}</div>
                    <input type="${getInputType()}" id="current-input" placeholder="Votre réponse..." class="chat-input">
                    <button onclick="submitAnswer()" class="btn" style="margin-top: 10px;">Valider</button>
                `;
            } else {
                messageDiv.textContent = text;
            }
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function getInputType() {
            const step = questions[currentStep];
            return step ? step.type : 'text';
        }
        
        function askNextQuestion() {
            if (currentStep < questions.length) {
                const step = questions[currentStep];
                addMessage(step.question, 'assistant');
                
                setTimeout(() => {
                    addMessage("Votre réponse :", 'assistant', true);
                }, 1000);
            } else {
                addMessage("Parfait ! Toutes les informations ont été collectées. Génération des documents en cours...", 'assistant');
                setTimeout(() => {
                    generateDocuments();
                }, 2000);
            }
        }
        
        function submitAnswer() {
            const input = document.getElementById('current-input');
            if (!input || !input.value.trim()) return;
            
            const answer = input.value.trim();
            const step = questions[currentStep];
            
            // Enregistrer la réponse
            formData[step.field] = answer;
            
            // Afficher la réponse de l'utilisateur
            addMessage(answer, 'user');
            
            // Passer à la question suivante
            currentStep++;
            
            setTimeout(() => {
                askNextQuestion();
            }, 1000);
        }
        
        function generateDocuments() {
            addMessage("✅ Documents générés avec succès !", 'assistant');
            addMessage("📄 Convocation à l'AG des associés", 'assistant');
            addMessage("📄 PV + Feuille de présence", 'assistant');
            addMessage("📄 PV d'AG seul", 'assistant');
            addMessage("📄 Rapport de gestion", 'assistant');
            addMessage("🎉 Tous vos documents juridiques sont prêts !", 'assistant');
        }
        
        function uploadFiles() {
            alert('Simulation - Fichiers téléchargés avec succès !\\nVous pouvez maintenant utiliser l\\'assistant conversationnel.');
        }
        
        // Initialisation
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                addMessage("Bonjour ! Je vais vous accompagner pour préparer votre Assemblée Générale. Commençons par quelques questions essentielles.", 'assistant');
                setTimeout(() => {
                    askNextQuestion();
                }, 2000);
            }, 1000);
        });
        
        // Gérer l'entrée au clavier
        document.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const currentInput = document.getElementById('current-input');
                if (currentInput) {
                    submitAnswer();
                }
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Page principale de l'application"""
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render_template_string(HTML_TEMPLATE, timestamp=timestamp)

@app.route('/test')
def test():
    """Test de santé de l'application"""
    return jsonify({
        'status': 'OK',
        'message': 'Application fonctionnelle',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Simulation d'upload de fichiers"""
    return jsonify({
        'status': 'success',
        'message': 'Fichiers téléchargés avec succès',
        'files_count': 5
    })

@app.route('/api/generate', methods=['POST'])
def generate_documents():
    """Simulation de génération de documents"""
    return jsonify({
        'status': 'success',
        'message': 'Documents générés avec succès',
        'documents': [
            'Convocation à l\'AG des associés',
            'PV + Feuille de présence',
            'PV d\'AG seul',
            'Rapport de gestion'
        ]
    })

if __name__ == '__main__':
    print("🚀 Démarrage du Générateur de Documents SAS")
    print("=" * 50)
    print("📁 Dossiers créés automatiquement")
    print("🌐 Application accessible sur : http://localhost:5000")
    print("🔧 Pour arrêter : Ctrl+C")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée proprement")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        print("💡 Essayez : pip install flask")