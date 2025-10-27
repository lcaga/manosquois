// Variables globales
let currentStep = 0;
let formData = {};
let uploadedFiles = {};
let extractedData = {};

// Étapes de la conversation
const conversationSteps = [
    {
        id: 'date_cloture',
        question: "Pour commencer, quelle est la date de clôture de l'exercice comptable que vous souhaitez approuver ?",
        type: 'date',
        field: 'date_cloture_exercice'
    },
    {
        id: 'date_ag',
        question: "Parfait. Quand souhaitez-vous tenir votre Assemblée Générale ?",
        helpText: "Rappel : l'AG doit se tenir dans les 6 mois suivant la date de clôture.",
        type: 'date_with_suggestions',
        field: 'date_assemblee_generale'
    },
    {
        id: 'heure_ag',
        question: "À quelle heure se tiendra l'assemblée ?",
        type: 'time_with_suggestions',
        field: 'heure_assemblee_generale',
        suggestions: ['9:00', '10:00', '14:30']
    },
    {
        id: 'lieu_ag',
        question: "Où se déroulera cette assemblée ?",
        type: 'location_with_suggestions',
        field: 'lieu_assemblee_generale'
    },
    {
        id: 'president',
        question: "Qui présidera la séance ?",
        type: 'president_with_suggestion',
        field: 'nom_prenom_president_de_seance'
    },
    {
        id: 'secretaire',
        question: "Très bien. Et pour finir, qui sera désigné(e) comme secrétaire de séance ?",
        type: 'text',
        field: 'nom_prenom_secretaire_de_seance',
        placeholder: "Nom et prénom..."
    }
];

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUploads();
    setupEventListeners();
});

function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            handleFileUpload(e.target);
        });
    });
}

function handleFileUpload(input) {
    const file = input.files[0];
    const statusElement = document.getElementById(input.id + '-status');
    const uploadItem = input.closest('.upload-item');
    
    if (file) {
        statusElement.textContent = `📄 ${file.name}`;
        uploadItem.classList.add('has-file');
        uploadedFiles[input.name] = file;
    } else {
        statusElement.textContent = 'Aucun fichier sélectionné';
        uploadItem.classList.remove('has-file');
        delete uploadedFiles[input.name];
    }
    
    checkAllFilesUploaded();
}

function checkAllFilesUploaded() {
    const requiredFiles = ['kbis', 'statuts', 'comptes_n1', 'comptes_n2', 'comptes_n3'];
    const continueBtn = document.getElementById('continue-btn');
    
    const allUploaded = requiredFiles.every(file => uploadedFiles[file]);
    
    continueBtn.disabled = !allUploaded;
    
    if (allUploaded) {
        continueBtn.textContent = '✅ Continuer vers les informations de l\'AG';
    }
}

function setupEventListeners() {
    const continueBtn = document.getElementById('continue-btn');
    const generateBtn = document.getElementById('generate-btn');
    
    continueBtn.addEventListener('click', startConversation);
    generateBtn.addEventListener('click', generateDocuments);
}

function startConversation() {
    // Cacher la section upload et afficher la section conversation
    document.getElementById('upload-section').style.display = 'none';
    document.getElementById('conversation-section').style.display = 'block';
    
    // Commencer la conversation
    currentStep = 0;
    showNextQuestion();
}

function addMessage(text, isUser = false, isHtml = false) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
    
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    
    if (isHtml) {
        bubbleDiv.innerHTML = text;
    } else {
        bubbleDiv.textContent = text;
    }
    
    messageDiv.appendChild(bubbleDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll vers le bas
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showNextQuestion() {
    if (currentStep >= conversationSteps.length) {
        finishConversation();
        return;
    }
    
    const step = conversationSteps[currentStep];
    
    // Ajouter la question de l'assistant
    addMessage(step.question);
    
    // Ajouter le texte d'aide si disponible
    if (step.helpText) {
        setTimeout(() => {
            addMessage(step.helpText);
        }, 500);
    }
    
    // Afficher les options d'input appropriées
    setTimeout(() => {
        showInputForStep(step);
    }, 1000);
}

function showInputForStep(step) {
    const chatInput = document.getElementById('chat-input');
    chatInput.innerHTML = '';
    
    const inputGroup = document.createElement('div');
    inputGroup.className = 'input-group';
    
    switch (step.type) {
        case 'date':
            showDateInput(inputGroup, step);
            break;
        case 'date_with_suggestions':
            showDateWithSuggestions(inputGroup, step);
            break;
        case 'time_with_suggestions':
            showTimeWithSuggestions(inputGroup, step);
            break;
        case 'location_with_suggestions':
            showLocationWithSuggestions(inputGroup, step);
            break;
        case 'president_with_suggestion':
            showPresidentWithSuggestion(inputGroup, step);
            break;
        case 'text':
            showTextInput(inputGroup, step);
            break;
    }
    
    chatInput.appendChild(inputGroup);
}

function showDateInput(container, step) {
    const input = document.createElement('input');
    input.type = 'date';
    input.id = step.field;
    input.required = true;
    
    const button = document.createElement('button');
    button.className = 'validate-btn';
    button.textContent = 'Valider';
    button.onclick = () => validateDateInput(step, input.value);
    
    container.appendChild(input);
    container.appendChild(button);
}

function showDateWithSuggestions(container, step) {
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'button-group';
    
    if (formData.date_cloture_exercice) {
        const clotureDate = new Date(formData.date_cloture_exercice);
        
        // Calculer les dates suggérées
        const date1 = new Date(clotureDate);
        date1.setMonth(date1.getMonth() + 5);
        date1.setDate(15);
        
        const date2 = new Date(clotureDate);
        date2.setMonth(date2.getMonth() + 6);
        
        const btn1 = document.createElement('button');
        btn1.className = 'option-btn';
        btn1.textContent = formatDateForDisplay(date1);
        btn1.onclick = () => selectDate(step, date1.toISOString().split('T')[0]);
        
        const btn2 = document.createElement('button');
        btn2.className = 'option-btn';
        btn2.textContent = `${formatDateForDisplay(date2)} (Date limite)`;
        btn2.onclick = () => selectDate(step, date2.toISOString().split('T')[0]);
        
        buttonGroup.appendChild(btn1);
        buttonGroup.appendChild(btn2);
    }
    
    const autreBtn = document.createElement('button');
    autreBtn.className = 'option-btn autre-choix';
    autreBtn.textContent = 'Choisir une autre date';
    autreBtn.onclick = () => showCustomDateInput(container, step);
    
    buttonGroup.appendChild(autreBtn);
    container.appendChild(buttonGroup);
}

function showCustomDateInput(container, step) {
    container.innerHTML = '';
    
    const input = document.createElement('input');
    input.type = 'date';
    input.id = step.field;
    
    // Définir la date max (6 mois après clôture)
    if (formData.date_cloture_exercice) {
        const clotureDate = new Date(formData.date_cloture_exercice);
        const maxDate = new Date(clotureDate);
        maxDate.setMonth(maxDate.getMonth() + 6);
        input.max = maxDate.toISOString().split('T')[0];
        input.min = new Date().toISOString().split('T')[0];
    }
    
    const button = document.createElement('button');
    button.className = 'validate-btn';
    button.textContent = 'Valider';
    button.onclick = () => validateCustomDate(step, input);
    
    const helpDiv = document.createElement('div');
    helpDiv.className = 'help-text';
    helpDiv.textContent = 'La date doit être dans les 6 mois suivant la clôture';
    
    container.appendChild(input);
    container.appendChild(button);
    container.appendChild(helpDiv);
}

function showTimeWithSuggestions(container, step) {
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'button-group';
    
    step.suggestions.forEach(time => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = time;
        btn.onclick = () => selectTime(step, time);
        buttonGroup.appendChild(btn);
    });
    
    const autreBtn = document.createElement('button');
    autreBtn.className = 'option-btn autre-choix';
    autreBtn.textContent = 'Choisir une autre heure';
    autreBtn.onclick = () => showCustomTimeInput(container, step);
    
    buttonGroup.appendChild(autreBtn);
    container.appendChild(buttonGroup);
}

function showCustomTimeInput(container, step) {
    container.innerHTML = '';
    
    const input = document.createElement('input');
    input.type = 'time';
    input.id = step.field;
    
    const button = document.createElement('button');
    button.className = 'validate-btn';
    button.textContent = 'Valider';
    button.onclick = () => validateTimeInput(step, input.value);
    
    container.appendChild(input);
    container.appendChild(button);
}

function showLocationWithSuggestions(container, step) {
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'button-group';
    
    const siegeBtn = document.createElement('button');
    siegeBtn.className = 'option-btn';
    siegeBtn.textContent = 'Au siège social';
    siegeBtn.onclick = () => selectLocation(step, extractedData.adresse_du_siege_social || 'Au siège social');
    
    const visioBtn = document.createElement('button');
    visioBtn.className = 'option-btn';
    visioBtn.textContent = 'En visioconférence';
    visioBtn.onclick = () => selectLocation(step, 'En visioconférence');
    
    const autreBtn = document.createElement('button');
    autreBtn.className = 'option-btn autre-choix';
    autreBtn.textContent = 'Autre lieu';
    autreBtn.onclick = () => showCustomLocationInput(container, step);
    
    buttonGroup.appendChild(siegeBtn);
    buttonGroup.appendChild(visioBtn);
    buttonGroup.appendChild(autreBtn);
    container.appendChild(buttonGroup);
}

function showCustomLocationInput(container, step) {
    container.innerHTML = '';
    
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Saisir l\'adresse complète...';
    input.id = step.field;
    
    const button = document.createElement('button');
    button.className = 'validate-btn';
    button.textContent = 'Valider';
    button.onclick = () => validateTextInput(step, input.value);
    
    container.appendChild(input);
    container.appendChild(button);
}

function showPresidentWithSuggestion(container, step) {
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'button-group';
    
    if (extractedData.nom_prenom_president_legal) {
        const presidentBtn = document.createElement('button');
        presidentBtn.className = 'option-btn';
        presidentBtn.textContent = extractedData.nom_prenom_president_legal;
        presidentBtn.onclick = () => selectPresident(step, extractedData.nom_prenom_president_legal);
        buttonGroup.appendChild(presidentBtn);
    }
    
    const autreBtn = document.createElement('button');
    autreBtn.className = 'option-btn autre-choix';
    autreBtn.textContent = 'Autre personne';
    autreBtn.onclick = () => showCustomPresidentInput(container, step);
    
    buttonGroup.appendChild(autreBtn);
    container.appendChild(buttonGroup);
}

function showCustomPresidentInput(container, step) {
    container.innerHTML = '';
    showTextInput(container, step);
}

function showTextInput(container, step) {
    const input = document.createElement('input');
    input.type = 'text';
    input.placeholder = step.placeholder || 'Votre réponse...';
    input.id = step.field;
    
    const button = document.createElement('button');
    button.className = 'validate-btn';
    if (currentStep === conversationSteps.length - 1) {
        button.textContent = 'Terminer';
    } else {
        button.textContent = 'Valider';
    }
    button.onclick = () => validateTextInput(step, input.value);
    
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            validateTextInput(step, input.value);
        }
    });
    
    container.appendChild(input);
    container.appendChild(button);
    
    // Focus sur l'input
    setTimeout(() => input.focus(), 100);
}

// Fonctions de validation et sélection
function validateDateInput(step, value) {
    if (!value) {
        showError('Veuillez sélectionner une date');
        return;
    }
    
    formData[step.field] = value;
    addMessage(formatDateForDisplay(new Date(value)), true);
    nextStep();
}

function selectDate(step, value) {
    formData[step.field] = value;
    addMessage(formatDateForDisplay(new Date(value)), true);
    nextStep();
}

function validateCustomDate(step, input) {
    const value = input.value;
    if (!value) {
        showError('Veuillez sélectionner une date');
        return;
    }
    
    // Vérifier la contrainte des 6 mois
    if (formData.date_cloture_exercice) {
        const clotureDate = new Date(formData.date_cloture_exercice);
        const selectedDate = new Date(value);
        const maxDate = new Date(clotureDate);
        maxDate.setMonth(maxDate.getMonth() + 6);
        
        if (selectedDate > maxDate) {
            showError('La date doit être dans les 6 mois suivant la clôture');
            return;
        }
    }
    
    formData[step.field] = value;
    addMessage(formatDateForDisplay(new Date(value)), true);
    nextStep();
}

function selectTime(step, value) {
    formData[step.field] = value;
    addMessage(value, true);
    nextStep();
}

function validateTimeInput(step, value) {
    if (!value) {
        showError('Veuillez sélectionner une heure');
        return;
    }
    
    formData[step.field] = value;
    addMessage(value, true);
    nextStep();
}

function selectLocation(step, value) {
    formData[step.field] = value;
    addMessage(value, true);
    nextStep();
}

function selectPresident(step, value) {
    formData[step.field] = value;
    addMessage(value, true);
    nextStep();
}

function validateTextInput(step, value) {
    if (!value || value.trim() === '') {
        showError('Veuillez saisir une réponse');
        return;
    }
    
    formData[step.field] = value.trim();
    addMessage(value.trim(), true);
    nextStep();
}

function showError(message) {
    const chatInput = document.getElementById('chat-input');
    const existingError = chatInput.querySelector('.error-text');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-text';
    errorDiv.textContent = message;
    chatInput.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 3000);
}

function nextStep() {
    currentStep++;
    
    // Nettoyer l'input
    document.getElementById('chat-input').innerHTML = '';
    
    setTimeout(() => {
        showNextQuestion();
    }, 1000);
}

function finishConversation() {
    addMessage("Parfait ! Toutes les informations ont été recueillies. Vous pouvez maintenant générer les documents.");
    
    setTimeout(() => {
        document.getElementById('conversation-section').style.display = 'none';
        document.getElementById('generation-section').style.display = 'block';
    }, 2000);
}

async function generateDocuments() {
    const generateBtn = document.getElementById('generate-btn');
    const progress = document.getElementById('progress');
    
    // Afficher le progrès
    generateBtn.style.display = 'none';
    progress.style.display = 'block';
    
    try {
        // Préparer les données à envoyer
        const formDataToSend = new FormData();
        
        // Ajouter les fichiers
        Object.keys(uploadedFiles).forEach(key => {
            formDataToSend.append(key, uploadedFiles[key]);
        });
        
        // Ajouter les données du formulaire
        Object.keys(formData).forEach(key => {
            formDataToSend.append(key, formData[key]);
        });
        
        // Envoyer la requête
        const response = await fetch('/generate', {
            method: 'POST',
            body: formDataToSend
        });
        
        const result = await response.json();
        
        if (result.success) {
            extractedData = result.extracted_data;
            showResults(result.files);
        } else {
            showGenerationError(result.error);
        }
        
    } catch (error) {
        console.error('Erreur:', error);
        showGenerationError('Erreur de connexion au serveur');
    }
}

function showResults(files) {
    document.getElementById('generation-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'block';
    
    const resultsGrid = document.getElementById('results');
    resultsGrid.innerHTML = '';
    
    // Organiser les fichiers par type
    const documents = {
        'PV + Feuille de présence': {
            docx: files.pv_feuille_docx,
            pdf: files.pv_feuille_pdf
        },
        'Convocation à l\'AG': {
            docx: files.convocation_docx,
            pdf: files.convocation_pdf
        }
    };
    
    Object.keys(documents).forEach(docName => {
        const doc = documents[docName];
        
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        
        const title = document.createElement('h3');
        title.textContent = docName;
        
        const downloadLinks = document.createElement('div');
        downloadLinks.className = 'download-links';
        
        if (doc.docx) {
            const docxLink = document.createElement('a');
            docxLink.href = `/download/${doc.docx}`;
            docxLink.className = 'download-link';
            docxLink.textContent = '📄 Télécharger Word';
            docxLink.download = doc.docx;
            downloadLinks.appendChild(docxLink);
        }
        
        if (doc.pdf) {
            const pdfLink = document.createElement('a');
            pdfLink.href = `/download/${doc.pdf}`;
            pdfLink.className = 'download-link pdf';
            pdfLink.textContent = '📕 Télécharger PDF';
            pdfLink.download = doc.pdf;
            downloadLinks.appendChild(pdfLink);
        }
        
        resultItem.appendChild(title);
        resultItem.appendChild(downloadLinks);
        resultsGrid.appendChild(resultItem);
    });
}

function showGenerationError(error) {
    document.getElementById('progress').style.display = 'none';
    document.getElementById('generate-btn').style.display = 'inline-flex';
    
    alert(`Erreur lors de la génération: ${error}`);
}

// Fonctions utilitaires
function formatDateForDisplay(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    return date.toLocaleDateString('fr-FR', options);
}