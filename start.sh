#!/bin/bash

echo "🚀 Générateur de Documents SAS - Démarrage"
echo "=========================================="

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 non trouvé. Veuillez installer Python 3.8+"
    exit 1
fi

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python3 -c "import flask" 2>/dev/null || {
    echo "⚠️  Flask non installé. Installation en cours..."
    pip install flask werkzeug --break-system-packages
}

# Arrêter l'ancienne instance si elle existe
echo "🔄 Arrêt des anciennes instances..."
pkill -f "python3 app_simple.py" 2>/dev/null || true

# Démarrer l'application
echo "🌟 Démarrage de l'application..."
echo "📂 Dossier de travail: $(pwd)"
echo "🌐 L'application sera accessible sur: http://localhost:5000"
echo ""
echo "✅ Pour tester l'application:"
echo "   - Interface web: http://localhost:5000"
echo "   - Test automatisé: python3 test_demo.py"
echo ""
echo "🔍 Logs de l'application:"
echo "----------------------------------------"

# Lancer l'application
python3 app_simple.py