"""
Configuration de l'application Reddit RAG Chatbot
Centralisez tous les paramètres configurables ici
"""

import os
from pathlib import Path

# ============================================================================
# CHEMINS ET FICHIERS
# ============================================================================

# Répertoire racine du projet
PROJECT_ROOT = Path(__file__).parent

# Fichiers du système RAG
RAG_INDEX_FILE = "reddit_optimized_rag_index.faiss"
RAG_CHUNKS_FILE = "reddit_optimized_rag_chunks.pkl"
RAG_METADATA_FILE = "reddit_optimized_rag_metadata.json"
RAG_CONVERSATIONS_FILE = "reddit_optimized_rag_conversations.pkl"

# Données source
DATA_DIR = PROJECT_ROOT / "reddit_data" / "raw"
DATA_FILE = DATA_DIR / "casual_data_windows.csv"

# Assets
ASSETS_DIR = PROJECT_ROOT / "assets"
CSS_FILE = ASSETS_DIR / "custom_styles.css"

# ============================================================================
# PARAMÈTRES DE L'APPLICATION
# ============================================================================

class AppConfig:
    """Configuration de l'application Dash"""
    
    # Serveur
    HOST = os.getenv("DASH_HOST", "127.0.0.1")
    PORT = int(os.getenv("DASH_PORT", 8050))
    DEBUG = os.getenv("DASH_DEBUG", "False").lower() == "true"
    
    # Titre et métadonnées
    TITLE = "Reddit RAG Chatbot"
    SUBTITLE = "Intelligence conversationnelle basée sur Reddit"
    VERSION = "1.0.0"
    
    # Thèmes
    BOOTSTRAP_THEME = "CYBORG"  # CYBORG, DARKLY, SLATE, etc.
    
    # Performance
    CACHE_TIMEOUT = 3600  # Secondes
    MAX_CHAT_HISTORY = 100  # Messages max en mémoire
    
# ============================================================================
# PARAMÈTRES RAG
# ============================================================================

class RAGConfig:
    """Configuration du système RAG"""
    
    # Modèle d'embeddings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    EMBEDDING_DIM = 384
    
    # Recherche
    DEFAULT_TOP_K = 3
    MIN_TOP_K = 1
    MAX_TOP_K = 10
    
    # Optimisations par défaut
    USE_RERANKING = True
    USE_DIVERSITY = True
    USE_HYBRID = False
    USE_CACHE = True
    
    # Filtres
    DEFAULT_MIN_LENGTH = 0
    DEFAULT_MAX_LENGTH = 5000
    
    # Qualité
    QUALITY_THRESHOLDS = {
        'excellent': 0.8,
        'good': 0.6,
        'fair': 0.4,
        'poor': 0.0
    }
    
    # Cache
    CACHE_TTL = 3600  # Time-to-live en secondes
    
    # Chunking
    CHUNK_STRATEGY = 'qa_pairs'  # 'qa_pairs' ou 'questions_only'
    MAX_CHUNK_LENGTH = 3000
    MIN_CHUNK_LENGTH = 10

# ============================================================================
# PARAMÈTRES LLM
# ============================================================================

class LLMConfig:
    """Configuration du générateur LLM"""
    
    # Backend
    DEFAULT_BACKEND = "llama-cpp"  # 'llama-cpp' ou 'huggingface'
    
    # Modèles
    MISTRAL_MODEL_REPO = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    MISTRAL_MODEL_FILE = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    
    PHI_MODEL_NAME = "microsoft/phi-2"
    TINYLLAMA_MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    
    # Génération
    DEFAULT_MAX_TOKENS = 512
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_TOP_P = 0.9
    
    MIN_TEMPERATURE = 0.1
    MAX_TEMPERATURE = 1.0
    
    # Contexte
    DEFAULT_N_CTX = 4096
    MIN_N_CTX = 2048
    MAX_N_CTX = 8192
    
    # CPU
    N_THREADS = os.cpu_count() or 4
    
    # Templates de prompts
    PROMPT_TEMPLATES = {
        'mistral': 'mistral',
        'phi': 'phi',
        'default': 'default'
    }
    DEFAULT_TEMPLATE = 'mistral'

# ============================================================================
# THÈMES ET COULEURS
# ============================================================================

class ThemeConfig:
    """Configuration des thèmes visuels"""
    
    DARK_THEME = {
        'name': 'dark',
        'background': '#0a0e27',
        'card': 'rgba(20, 25, 45, 0.95)',
        'text': '#e0e0e0',
        'primary': '#00d4ff',
        'secondary': '#9d4edd',
        'success': '#06ffa5',
        'warning': '#ffbe0b',
        'danger': '#ff006e',
        'info': '#4cc9f0'
    }
    
    LIGHT_THEME = {
        'name': 'light',
        'background': '#f8f9fa',
        'card': 'rgba(255, 255, 255, 0.95)',
        'text': '#212529',
        'primary': '#0077b6',
        'secondary': '#6c757d',
        'success': '#06d6a0',
        'warning': '#ffd166',
        'danger': '#ef476f',
        'info': '#4cc9f0'
    }
    
    # Thème actif
    CURRENT_THEME = DARK_THEME
    
    # Icônes Font Awesome
    ICONS = {
        'robot': 'fas fa-robot',
        'user': 'fas fa-user-circle',
        'search': 'fas fa-search',
        'settings': 'fas fa-sliders-h',
        'stats': 'fas fa-chart-line',
        'quality': 'fas fa-star',
        'export': 'fas fa-download',
        'clear': 'fas fa-broom',
        'send': 'fas fa-paper-plane',
        'examples': 'fas fa-lightbulb',
        'time': 'fas fa-clock',
        'cache': 'fas fa-bolt',
        'brain': 'fas fa-brain',
        'magic': 'fas fa-magic',
        'filter': 'fas fa-filter'
    }

# ============================================================================
# CONTENU ET TEXTES
# ============================================================================

class ContentConfig:
    """Configuration du contenu textuel"""
    
    # Questions d'exemple
    EXAMPLE_QUESTIONS = [
        "What's the best phone to buy?",
        "How do I stay motivated?",
        "What should I do when feeling sad?",
        "Best advice for learning programming?",
        "How to make new friends?",
        "What are good movies to watch?",
        "How to start working out?",
        "Best diet for weight loss?",
        "Tips for better sleep?",
        "What laptop is good for students?",
        "How to deal with stress?",
        "Best productivity tips?",
        "How to learn a new language?",
        "What career should I choose?",
        "How to save money effectively?"
    ]
    
    # Messages système
    MESSAGES = {
        'welcome': "👋 Bienvenue ! Posez-moi n'importe quelle question.",
        'no_results': "❌ Désolé, je n'ai pas trouvé de réponse pertinente.",
        'error': "⚠️ Une erreur s'est produite. Veuillez réessayer.",
        'system_unavailable': "🔧 Système RAG non disponible.",
        'loading': "⏳ Recherche en cours...",
        'llm_generating': "🧠 Génération de la réponse...",
        'cache_hit': "⚡ Réponse récupérée du cache",
    }
    
    # Tooltips
    TOOLTIPS = {
        'num_results': "Nombre de résultats à afficher (plus = plus d'informations)",
        'reranking': "Re-classe les résultats pour améliorer la pertinence",
        'diversity': "Évite les résultats trop similaires entre eux",
        'hybrid': "Combine recherche sémantique et mots-clés",
        'llm': "Active la génération de réponses synthétisées par IA",
        'temperature': "Contrôle la créativité (élevé = plus créatif)",
        'min_length': "Longueur minimale des réponses en caractères",
        'max_length': "Longueur maximale des réponses en caractères"
    }
    
    # Labels
    LABELS = {
        'num_results': "Nombre de résultats",
        'optimizations': "Optimisations",
        'reranking': "Re-classement des résultats",
        'diversity': "Diversification",
        'hybrid': "Recherche hybride",
        'llm_mode': "Mode Génératif",
        'temperature': "Température",
        'filters': "Filtres de longueur",
        'min_length': "Longueur minimale",
        'max_length': "Longueur maximale",
        'clear': "Effacer la conversation",
        'export': "Exporter JSON",
        'send': "Envoyer",
        'user': "Vous",
        'assistant': "Assistant"
    }

# ============================================================================
# PARAMÈTRES DE PERFORMANCE
# ============================================================================

class PerformanceConfig:
    """Configuration des paramètres de performance"""
    
    # Limites
    MAX_MESSAGE_LENGTH = 1000  # Caractères
    MAX_RESULTS_DISPLAY = 10
    MAX_EXPORT_MESSAGES = 1000
    
    # Timeouts
    SEARCH_TIMEOUT = 30  # Secondes
    LLM_TIMEOUT = 60  # Secondes
    
    # Batch processing
    EMBEDDING_BATCH_SIZE = 32
    SEARCH_BATCH_SIZE = 100
    
    # Cache
    ENABLE_CACHE = True
    CACHE_SIZE_LIMIT = 1000  # Nombre d'entrées
    
    # Logging
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
    LOG_FILE = PROJECT_ROOT / "app.log"
    ENABLE_FILE_LOGGING = False

# ============================================================================
# PARAMÈTRES DE SÉCURITÉ
# ============================================================================

class SecurityConfig:
    """Configuration de sécurité"""
    
    # Rate limiting
    ENABLE_RATE_LIMIT = False
    MAX_REQUESTS_PER_MINUTE = 60
    MAX_REQUESTS_PER_HOUR = 1000
    
    # Input validation
    MAX_INPUT_LENGTH = 1000
    ALLOWED_CHARACTERS = r'^[a-zA-Z0-9\s\.,!?\'\"-]+$'
    
    # CORS (si déployé)
    CORS_ALLOWED_ORIGINS = ["http://localhost:*"]

# ============================================================================
# PARAMÈTRES DE DÉPLOIEMENT
# ============================================================================

class DeploymentConfig:
    """Configuration pour le déploiement"""
    
    # Environnement
    ENVIRONMENT = os.getenv("ENV", "development")  # development, staging, production
    
    # URLs
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8050")
    
    # Monitoring
    ENABLE_ANALYTICS = False
    ANALYTICS_ID = os.getenv("ANALYTICS_ID", "")
    
    # Error tracking
    ENABLE_SENTRY = False
    SENTRY_DSN = os.getenv("SENTRY_DSN", "")
    
    # Database (pour persistance future)
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    # Redis (pour cache distribué)
    REDIS_URL = os.getenv("REDIS_URL", "")

# ============================================================================
# CONFIGURATION GLOBALE
# ============================================================================

class Config:
    """Configuration globale de l'application"""
    
    App = AppConfig
    RAG = RAGConfig
    LLM = LLMConfig
    Theme = ThemeConfig
    Content = ContentConfig
    Performance = PerformanceConfig
    Security = SecurityConfig
    Deployment = DeploymentConfig
    
    @classmethod
    def get_summary(cls):
        """Obtenir un résumé de la configuration"""
        return {
            'app': {
                'title': cls.App.TITLE,
                'version': cls.App.VERSION,
                'host': cls.App.HOST,
                'port': cls.App.PORT,
                'debug': cls.App.DEBUG
            },
            'rag': {
                'model': cls.RAG.EMBEDDING_MODEL,
                'default_top_k': cls.RAG.DEFAULT_TOP_K,
                'use_cache': cls.RAG.USE_CACHE
            },
            'llm': {
                'backend': cls.LLM.DEFAULT_BACKEND,
                'temperature': cls.LLM.DEFAULT_TEMPERATURE,
                'max_tokens': cls.LLM.DEFAULT_MAX_TOKENS
            },
            'theme': {
                'name': cls.Theme.CURRENT_THEME['name'],
                'primary': cls.Theme.CURRENT_THEME['primary']
            },
            'environment': cls.Deployment.ENVIRONMENT
        }
    
    @classmethod
    def print_summary(cls):
        """Afficher un résumé de la configuration"""
        summary = cls.get_summary()
        
        print("\n" + "="*70)
        print("📋 CONFIGURATION DE L'APPLICATION")
        print("="*70)
        
        for category, values in summary.items():
            print(f"\n{category.upper()}:")
            for key, value in values.items():
                print(f"  • {key}: {value}")
        
        print("\n" + "="*70)

# ============================================================================
# VALIDATION DE LA CONFIGURATION
# ============================================================================

def validate_config():
    """Valider la configuration"""
    errors = []
    warnings = []
    
    # Vérifier les fichiers RAG
    if not Path(RAG_INDEX_FILE).exists():
        errors.append(f"Fichier index RAG manquant: {RAG_INDEX_FILE}")
    
    if not Path(RAG_CHUNKS_FILE).exists():
        errors.append(f"Fichier chunks RAG manquant: {RAG_CHUNKS_FILE}")
    
    # Vérifier les plages de valeurs
    if not (1 <= RAGConfig.DEFAULT_TOP_K <= RAGConfig.MAX_TOP_K):
        errors.append(f"DEFAULT_TOP_K invalide: {RAGConfig.DEFAULT_TOP_K}")
    
    if not (LLMConfig.MIN_TEMPERATURE <= LLMConfig.DEFAULT_TEMPERATURE <= LLMConfig.MAX_TEMPERATURE):
        warnings.append(f"DEFAULT_TEMPERATURE hors plage recommandée: {LLMConfig.DEFAULT_TEMPERATURE}")
    
    # Vérifier les dossiers
    if not ASSETS_DIR.exists():
        warnings.append(f"Dossier assets manquant: {ASSETS_DIR}")
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Afficher les résultats
    if errors:
        print("\n❌ ERREURS DE CONFIGURATION:")
        for error in errors:
            print(f"  • {error}")
    
    if warnings:
        print("\n⚠️  AVERTISSEMENTS:")
        for warning in warnings:
            print(f"  • {warning}")
    
    if not errors and not warnings:
        print("\n✅ Configuration validée avec succès!")
    
    return len(errors) == 0

# ============================================================================
# EXPORT
# ============================================================================

# Instance globale
config = Config()

# Export pour imports simplifiés
__all__ = [
    'Config',
    'config',
    'AppConfig',
    'RAGConfig',
    'LLMConfig',
    'ThemeConfig',
    'ContentConfig',
    'PerformanceConfig',
    'SecurityConfig',
    'DeploymentConfig',
    'validate_config'
]

# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    print("\n🧪 TEST DE LA CONFIGURATION\n")
    
    # Afficher le résumé
    Config.print_summary()
    
    # Valider
    validate_config()
    
    # Tester l'accès aux valeurs
    print("\n📝 EXEMPLES D'UTILISATION:")
    print(f"  from config import config")
    print(f"  config.App.TITLE = '{Config.App.TITLE}'")
    print(f"  config.RAG.DEFAULT_TOP_K = {Config.RAG.DEFAULT_TOP_K}")
    print(f"  config.Theme.CURRENT_THEME['primary'] = '{Config.Theme.CURRENT_THEME['primary']}'")
