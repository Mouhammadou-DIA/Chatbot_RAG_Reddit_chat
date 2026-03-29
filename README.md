# Reddit RAG Chatbot 

Chatbot RAG (Retrieval-Augmented Generation) basé sur des conversations Reddit, avec API FastAPI et frontend HTML/JS.

## Fonctionnalités

- **Pipeline RAG** : embeddings vectoriels + recherche sémantique + génération LLM
- **Support multilingue** : `paraphrase-multilingual-MiniLM-L12-v2`
- **Fournisseurs LLM** : Ollama (local), OpenAI, Anthropic, Groq
- **Reranking & cache** : amélioration de la pertinence et réduction de la latence
- **Rate limiting** : protection intégrée
- **API REST + frontend statique** : UI simple en HTML/CSS/JS
- **Déploiement Docker** : configuration prête à l'emploi

## Démarrage rapide

### Prérequis

- Python 3.10+
- [Ollama](https://ollama.ai/) (optionnel, pour un LLM local)

### Installation

```bash
git clone https://github.com/Mouhammadou-DIA/Chatbot_RAG_Reddit_chat.git
cd Chatbot_RAG_Reddit_chat
python -m venv venv
source venv/bin/activate       # Linux/Mac
# ou .\venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
```

### Préparer les données

```bash
python scripts/prepare_data.py
python scripts/index_conversations.py
```

### Lancer l'application

```bash
python run_api.py       # API
python run_frontend.py  # Frontend (autre terminal)
```

| Service   | URL                          |
|-----------|------------------------------|
| API       | http://localhost:8000        |
| Docs API  | http://localhost:8000/docs   |
| Frontend  | http://localhost:3000        |

## Structure du projet

```
Chatbot_RAG_Reddit_chat/
├── api/           # API FastAPI
│   ├── main.py    # App FastAPI
│   ├── routes/    # Endpoints
│   └── schemas/   # Schémas requête/réponse
├── src/
│   ├── config/    # Configuration et logs
│   ├── core/      # Composants RAG (embeddings, vector store, LLM)
│   ├── services/  # Logique métier
│   ├── models/    # Modèles Pydantic
│   └── utils/     # Utilitaires
├── frontend/      # UI HTML/CSS/JS
├── scripts/       # Préparation des données, indexation, benchmark
├── docs/          # Documentation (API, architecture, déploiement)
├── docker/        # Dockerfile + docker-compose
├── data/          # Données brutes, préparées et index vectoriel
├── logs/          # Logs d'exécution
└── tests/         # Tests unitaires et d'intégration
```

## Configuration

La configuration passe par des variables d'environnement. Voir `.env.example`.

| Variable | Description | Valeur par défaut |
|---|---|---|
| `API_HOST` | Hôte de l'API | `0.0.0.0` |
| `API_PORT` | Port de l'API | `8000` |
| `LLM_PROVIDER` | Backend LLM | `ollama` |
| `LLM_MODEL` | Modèle LLM | `llama3.1:8b` |
| `GROQ_API_KEY` | Clé Groq (optionnel) | — |
| `EMBEDDING_MODEL` | Modèle d'embeddings | `paraphrase-multilingual-MiniLM-L12-v2` |
| `CHROMA_PERSIST_DIRECTORY` | Dossier ChromaDB | `./data/vector_db` |
| `ENABLE_AUTH` | Auth JWT | `false` |

## Utilisation de l'API

Base URL : `http://localhost:8000`

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Informations de l'API |
| POST | `/api/v1/chat/` | Chat |
| GET | `/api/v1/chat/stats` | Statistiques |
| GET | `/api/v1/chat/examples` | Exemples |
| GET | `/api/v1/health/` | Health check |
| GET | `/api/v1/health/ready` | Readiness |
| GET | `/api/v1/health/live` | Liveness |
| GET | `/api/v1/health/version` | Version |

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Que penses-tu de l'\''IA ?", "use_llm": true, "n_results": 5, "temperature": 0.7, "max_tokens": 500}'
```

## Architecture

```
Indexation  : CSV Reddit → Nettoyage → Embeddings → ChromaDB
Inférence   : Question → Validation → Embedding → Recherche → Contexte → LLM → Réponse
```

Voir `docs/ARCHITECTURE.md` pour le détail.

## Docker

```bash
docker-compose -f docker/docker-compose.yml up -d
docker-compose -f docker/docker-compose.yml logs -f
```

## Développement

```bash
pip install -e ".[dev]"
pre-commit install
pytest
ruff check . && ruff format .
mypy src/
python scripts/benchmark.py
```

## Contribuer

1. Forker le dépôt
2. Créer une branche : `git checkout -b feature/ma-feature`
3. Committer : `git commit -m 'Ma feature'`
4. Pousser : `git push origin feature/ma-feature`
5. Ouvrir une Pull Request
