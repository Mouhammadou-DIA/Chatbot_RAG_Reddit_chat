# 🚀 Guide de Démarrage Rapide - Reddit RAG Chatbot Dash

Guide ultra-rapide pour démarrer l'application en 5 minutes !

---

## ⚡ Démarrage Express (TL;DR)

```bash
# 1. Installer les dépendances
pip install dash dash-bootstrap-components plotly pandas numpy

# 2. Lancer l'application
python launch_dash_app.py

# 3. Ouvrir dans le navigateur
http://localhost:8050
```

---

## 📦 Installation Complète

### Étape 1: Vérifier Python

```bash
python --version  # Devrait afficher 3.8+
```

Si Python n'est pas installé : [Télécharger Python](https://www.python.org/downloads/)

### Étape 2: Installer les packages

**Option A : Installation automatique**
```bash
python launch_dash_app.py
# Le script vous proposera d'installer les dépendances manquantes
```

**Option B : Installation manuelle**
```bash
pip install dash dash-bootstrap-components plotly pandas numpy
pip install sentence-transformers faiss-cpu  # Si pas déjà fait
```

### Étape 3: Vérifier le système RAG

Le système RAG doit être construit au préalable. Si ce n'est pas fait :

```bash
python reddit_rag_optimized.py
```

Suivez les instructions pour construire l'index (15-20 minutes).

---

## 🎯 Utilisation de Base

### Lancement Simple

```bash
python launch_dash_app.py
```

### Options de Lancement

```bash
# Port personnalisé
python launch_dash_app.py --port 8080

# Mode debug (rechargement automatique)
python launch_dash_app.py --debug

# Accessible depuis le réseau local
python launch_dash_app.py --host 0.0.0.0

# Lancement rapide (sans vérifications)
python launch_dash_app.py --quick
```

### Interface Web

1. **Ouvrir le navigateur** : `http://localhost:8050`

2. **Poser une question** : Tapez dans la zone de texte en bas

3. **Ajuster les paramètres** : Utilisez la sidebar à gauche
   - Nombre de résultats : 1-10
   - Optimisations : Cochez/décochez
   - Filtres : Longueur min/max

4. **Voir les résultats** : Les réponses s'affichent dans la zone centrale

5. **Analyser** : Consultez les stats et la qualité à droite

---

## 🎨 Fonctionnalités Principales

### 1. Chat Interactif

- **Tapez votre question** dans la zone de saisie
- **Appuyez sur Entrée** ou cliquez sur le bouton d'envoi
- **Visualisez la réponse** avec les sources Reddit

**Exemple :**
```
Vous : What's the best phone to buy?

Assistant : 
🎯 Résultat 1 (Pertinence: 92.3%)
Q: Best smartphone under $500?
R: iPhone 13 or Google Pixel 7...
```

### 2. Questions Suggérées

- Cliquez sur une **question suggérée** dans la sidebar
- Elle sera automatiquement envoyée

### 3. Paramètres Avancés

**Nombre de résultats (1-10)**
- Plus = plus d'informations
- Moins = réponses plus ciblées

**Optimisations**
- ✅ **Re-classement** : Améliore la pertinence (+10-15%)
- ✅ **Diversification** : Évite la redondance
- ⬜ **Hybride** : Combine sémantique + mots-clés

**Filtres de longueur**
- Min : 0-1000 caractères
- Max : 500-5000 caractères

### 4. Mode LLM (Optionnel)

Si le LLM est configuré :
- ✅ Cochez "Activer le LLM"
- 🌡️ Ajustez la température (créativité)
- 🧠 Obtenez des réponses synthétisées

### 5. Statistiques

- ⏱️ **Temps moyen** : Rapidité des recherches
- 🔍 **Requêtes totales** : Nombre de questions posées
- ⚡ **Cache hits** : Taux d'utilisation du cache

### 6. Évaluation Qualité

- 🌟 **Excellent** : Confiance > 80%
- ✅ **Bon** : Confiance 60-80%
- 👍 **Moyen** : Confiance 40-60%
- ⚠️ **Faible** : Confiance < 40%

### 7. Export

- 💾 **Exporter JSON** : Sauvegarder la conversation
- 🗑️ **Effacer** : Réinitialiser l'historique

---

## 📊 Exemples de Questions

### Technologie
```
What's the best laptop for programming?
How do I learn Python?
Which smartphone has the best camera?
```

### Vie Quotidienne
```
How to stay motivated when studying?
Best advice for making friends?
How do I manage stress at work?
```

### Santé & Fitness
```
How to start working out as a beginner?
What's a good diet for weight loss?
Tips for better sleep quality?
```

### Divertissement
```
What are some good sci-fi movies?
Best video games to play in 2024?
Book recommendations for fiction lovers?
```

---

## ⚙️ Configuration Rapide

### Changer le Port

```bash
# Méthode 1 : Ligne de commande
python launch_dash_app.py --port 8080

# Méthode 2 : Variable d'environnement
export DASH_PORT=8080
python launch_dash_app.py

# Méthode 3 : Modifier config.py
# Dans config.py, changer:
PORT = 8080
```

### Changer le Thème

Dans `config.py` :
```python
# Passer au thème clair
CURRENT_THEME = LIGHT_THEME

# Ou personnaliser
CURRENT_THEME = {
    'primary': '#FF6B6B',  # Votre couleur
    # ...
}
```

### Personnaliser les Questions

Dans `config.py` :
```python
EXAMPLE_QUESTIONS = [
    "Votre question personnalisée 1",
    "Votre question personnalisée 2",
    # ...
]
```

---

## 🐛 Résolution de Problèmes

### Problème : "Module dash not found"

**Solution :**
```bash
pip install dash dash-bootstrap-components
```

### Problème : "Port already in use"

**Solution 1 :** Utiliser un autre port
```bash
python launch_dash_app.py --port 8051
```

**Solution 2 :** Tuer le processus
```bash
# Linux/Mac
lsof -ti:8050 | xargs kill -9

# Windows
netstat -ano | findstr :8050
taskkill /PID <PID> /F
```

### Problème : "Système RAG non disponible"

**Solution :**
```bash
# Construire le système RAG
python reddit_rag_optimized.py
```

### Problème : Page blanche

**Solution :**
1. Vérifier la console du navigateur (F12)
2. Vérifier les logs du serveur
3. Relancer en mode debug :
   ```bash
   python launch_dash_app.py --debug
   ```

### Problème : Recherches lentes

**Solutions :**
- Désactiver les optimisations (sidebar)
- Réduire le nombre de résultats
- Vérifier l'utilisation CPU/RAM

---

## 💡 Astuces et Bonnes Pratiques

### Pour les Meilleures Résultats

1. **Soyez spécifique** : Plus la question est précise, meilleures sont les réponses
   
   ❌ "How to learn?"
   ✅ "How to learn Python programming as a beginner?"

2. **Utilisez le re-classement** : Toujours activé par défaut

3. **Ajustez le nombre de résultats** :
   - 1-3 : Questions simples
   - 4-7 : Questions complexes
   - 8-10 : Recherche exploratoire

4. **Explorez les optimisations** :
   - Re-classement : Presque toujours bénéfique
   - Diversité : Pour des perspectives variées
   - Hybride : Pour des termes techniques précis

### Performance

1. **Cache** : Les questions répétées sont ~90% plus rapides

2. **Temps de réponse typiques** :
   - Recherche simple : 15-30 ms
   - Recherche optimisée : 30-50 ms
   - Génération LLM : 2-5 secondes

3. **Optimisation mémoire** :
   - Effacer régulièrement l'historique
   - Limiter le nombre de résultats

---

## 🔧 Personnalisation Avancée

### Modifier les Couleurs

`assets/custom_styles.css` :
```css
:root {
    --primary-color: #YOUR_COLOR;
    --success-color: #YOUR_COLOR;
}
```

### Ajouter une Nouvelle Métrique

Dans `reddit_rag_dash_app.py` :
```python
# Ajouter dans create_stats_panel()
dbc.Col([
    html.Div([
        html.I(className="fas fa-icon"),
        html.H4("Valeur", id="new-stat"),
        html.Small("Description")
    ])
], width=4)

# Ajouter le callback
@app.callback(
    Output("new-stat", "children"),
    Input("rag-stats", "data")
)
def update_new_stat(stats):
    return f"{stats.get('new_value', 0)}"
```

### Ajouter un Nouveau Filtre

Dans `create_sidebar()` :
```python
html.Label("Nouveau Filtre"),
dcc.Dropdown(
    id="new-filter",
    options=[...],
    value=default
)
```

---

## 📞 Support

### Documentation Complète

Consultez `README_DASH_APP.md` pour :
- Architecture détaillée
- API complète
- Exemples avancés
- Déploiement

### Ressources

- [Documentation Dash](https://dash.plotly.com/)
- [Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
- [Plotly](https://plotly.com/python/)

### Contact

- 📧 Email : your.email@example.com
- 🐛 Issues : [GitHub Issues](https://github.com/yourrepo/issues)

---

## 🎉 C'est Parti !

Vous êtes prêt ! Lancez l'application et explorez :

```bash
python launch_dash_app.py
```

Puis ouvrez : **http://localhost:8050**

---

**Bon chat ! 🤖💬**
